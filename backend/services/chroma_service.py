# backend/services/chroma_service.py

# 한글 주석 포함
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document as LC_Document
from docx import Document as DocxDocument
from config import config
import os
from tqdm import tqdm  # 진행률 표시를 위한 tqdm 추가
import glob
import importlib
from core.embeddings.hf_embedding import get_hf_embedding
from langchain_openai import OpenAIEmbeddings
from common.logger import setup_logger
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from core.parsers.document_loader import load_documents
import logging
from chromadb import Client, Settings
from chromadb.config import Settings as ChromaSettings
from core.utils import get_func_from_str
from config import get_config
import numpy as np

# 로거 설정
logger = logging.getLogger(__name__)

# 설정 로드
config = get_config()

# OpenAI 임베딩 모델 초기화
embeddings = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small"
)

# ChromaDB 클라이언트 초기화
client = Client(ChromaSettings(
    persist_directory=config.RAG_CHROMA_DIR,
    anonymized_telemetry=False
))

def initialize_collections():
    """모든 컬렉션 초기화 (DB -> RAG 순서)"""
    try:
        # 1. DB 컬렉션 초기화
        initialize_db_collections()
        logger.info("[CHROMA] DB 컬렉션 초기화 완료")
        
        # 2. RAG 컬렉션 초기화
        initialize_rag_collections()
        logger.info("[CHROMA] RAG 컬렉션 초기화 완료")
        
    except Exception as e:
        logger.error(f"[CHROMA] 컬렉션 초기화 중 오류 발생: {str(e)}")
        raise

def initialize_rag_collections():
    """
    config.RAG_CHROMA_COLLECTIONS 기반으로 여러 문서/이미지/컬렉션을 일괄 초기화
    - glob 패턴이 path에 들어오면 모든 파일을 반복 처리
    """
    for item in config.RAG_CHROMA_COLLECTIONS:
        print(f"\n[초기화] {item['collection']} ({item['type']}) - {item['path']}")
        docs = []
        
        # 1. 파일 목록 수집
        if item["type"] in ["file", "docx", "pdf", "txt"]:
            if "*" in item["path"]:
                # glob 패턴으로 여러 파일 처리
                for file_path in glob.glob(item["path"]):
                    print(f"[파일] {file_path}")
                    docs.extend(load_documents(file_path))
            else:
                # 단일 파일 처리
                print(f"[파일] {item['path']}")
                docs.extend(load_documents(item["path"]))
        
        if not docs:
            logger.warning(f"{item['collection']}에 변환할 문서가 없습니다.")
            continue
            
        try:
            # 2. 임베딩 모델 초기화
            embeddings = get_hf_embedding(item["embedding_model"])
            
            # 3. 컬렉션 생성 또는 가져오기
            if item["collection"] not in client.list_collections():
                collection = client.create_collection(
                    name=item["collection"],
                    metadata={
                        "hnsw:space": item.get("hnsw:space", "cosine"),
                        "hnsw:construction_ef": item.get("hnsw:construction_ef", 200),
                        "hnsw:search_ef": item.get("hnsw:search_ef", 200),
                        "hnsw:M": item.get("hnsw:M", 32),
                        "embedding_model": item["embedding_model"],
                        "type": item["type"],
                        "parser": item["parser"],
                        "search_top_k": item["search_top_k"],
                        "similarity_threshold": item.get("similarity_threshold", 0.6)
                    }
                )
            else:
                collection = client.get_collection(item["collection"])
            
            # 4. 문서 임베딩 생성 및 저장
            texts = [doc.page_content for doc in docs]
            metadatas = [doc.metadata for doc in docs]
            embeddings_list = embeddings.embed_documents(texts)
            
            # 5. 컬렉션에 추가
            collection.add(
                documents=texts,
                embeddings=embeddings_list,
                metadatas=metadatas,
                ids=[str(i) for i in range(len(docs))]
            )
            
            print(f"✓ {item['collection']}에 {len(docs)}개 문서 임베딩 저장 완료.")
            
        except Exception as e:
            logger.error(f"[CHROMA] {item['collection']} 처리 중 오류 발생: {str(e)}")
            continue

def initialize_db_collections():
    """DB 컬렉션 초기화"""
    try:
        # 컬렉션 설정 로드
        collections = config.DB_CHROMA_COLLECTIONS
        
        # 각 컬렉션 초기화
        for item in collections:
            collection_name = item["collection"]
            logger.info(f"[CHROMA] 컬렉션 초기화 시작: {collection_name}")
            
            try:
                # 1. 기존 컬렉션 삭제
                if collection_name in client.list_collections():
                    client.delete_collection(collection_name)
                    logger.info(f"[CHROMA] 기존 컬렉션 삭제됨: {collection_name}")
                
                # 2. 새 컬렉션 생성
                metadata = {
                    "hnsw:space": item.get("hnsw:space", "cosine"),
                    "hnsw:construction_ef": item.get("hnsw:construction_ef", 100),
                    "hnsw:search_ef": item.get("hnsw:search_ef", 100),
                    "hnsw:M": item.get("hnsw:M", 16),
                    "embedding_model": item["embedding_model"],
                    "type": item["type"],
                    "parser": item["parser"],
                    "search_top_k": item["search_top_k"],
                    "similarity_threshold": item.get("similarity_threshold", 0.8)  # DB 컬렉션은 더 높은 임계값 사용
                }
                
                collection = client.create_collection(
                    name=collection_name,
                    metadata=metadata
                )
                logger.info(f"[CHROMA] 새 컬렉션 생성됨: {collection_name} (metadata: {metadata})")
                
                # 3. 데이터 로드 함수 가져오기
                get_all_func = get_func_from_str(item["get_all_func"])
                to_doc_func = get_func_from_str(item["to_doc_func"])
                
                # 4. 데이터 로드 및 변환
                raw_docs = get_all_func()
                documents = [to_doc_func(doc) for doc in raw_docs]
                
                # 5. 데이터가 있으면 컬렉션 업데이트
                if documents:
                    # metadata에서 None 값 제거
                    filtered_metadatas = []
                    valid_docs = []
                    valid_texts = []
                    
                    for doc in documents:
                        # 5-1. 문서 내용 검증
                        if not doc.page_content or len(doc.page_content.strip()) == 0:
                            logger.warning(f"[CHROMA] 빈 문서 내용 발견, 건너뜀")
                            continue
                            
                        # 5-2. metadata 필터링
                        metadata = {k: v for k, v in doc.metadata.items() if v is not None}
                        filtered_metadatas.append(metadata)
                        valid_docs.append(doc)
                        valid_texts.append(doc.page_content)
                        
                        # 5-3. chatbot_collection인 경우 문서 내용 로깅
                        if collection_name == "chatbot_collection":
                            logger.info(f"[CHROMA] 추가 문서: pattern_id={metadata.get('pattern_id')}, "
                                      f"pattern={doc.page_content[:100]}..., "
                                      f"domain={metadata.get('domain')}, "
                                      f"category={metadata.get('category')}, "
                                      f"threshold={metadata.get('similarity_threshold')}")
                    
                    if not valid_docs:
                        logger.warning(f"[CHROMA] 유효한 문서가 없습니다: {collection_name}")
                        continue
                    
                    try:
                        # 6. 임베딩 모델 초기화
                        embeddings = get_hf_embedding(item["embedding_model"])
                        
                        # 7. 문서 임베딩 생성
                        embeddings_list = embeddings.embed_documents(valid_texts)
                        
                        # 7-1. 임베딩 정상 여부 체크
                        if not embeddings_list or len(embeddings_list) == 0:
                            raise ValueError("임베딩 생성 실패: 빈 임베딩 리스트")
                            
                        # 7-2. 임베딩 차원 체크
                        embedding_dim = len(embeddings_list[0])
                        if embedding_dim != 384:  # KR-SBERT-V40K-klueNLI-augSTS 모델의 차원
                            raise ValueError(f"임베딩 차원 불일치: {embedding_dim} != 384")
                            
                        # 7-3. 임베딩 값 체크 및 NaN/Inf 처리
                        valid_embeddings = []
                        valid_metadatas = []
                        valid_texts_filtered = []
                        
                        for i, (emb, meta, text) in enumerate(zip(embeddings_list, filtered_metadatas, valid_texts)):
                            if any(np.isnan(x) for x in emb) or any(np.isinf(x) for x in emb):
                                logger.warning(f"[CHROMA] 문서 {i}의 임베딩에 nan/inf 값 포함, 건너뜀")
                                continue
                            valid_embeddings.append(emb)
                            valid_metadatas.append(meta)
                            valid_texts_filtered.append(text)
                        
                        if not valid_embeddings:
                            raise ValueError("모든 임베딩이 유효하지 않음")
                        
                        logger.info(f"[CHROMA] 임베딩 생성 완료: {len(valid_embeddings)}개 문서, 차원={embedding_dim}")
                        
                        # 8. 새 데이터 추가 (임베딩 포함)
                        collection.add(
                            documents=valid_texts_filtered,
                            embeddings=valid_embeddings,
                            metadatas=valid_metadatas,
                            ids=[str(i) for i in range(len(valid_embeddings))]
                        )
                        logger.info(f"[CHROMA] {len(valid_embeddings)}개 문서 추가됨: {collection_name}")
                        
                    except Exception as e:
                        logger.error(f"[CHROMA] 임베딩 생성/저장 중 오류 발생: {str(e)}")
                        raise
                else:
                    logger.warning(f"[CHROMA] 추가할 문서 없음: {collection_name}")
                    
            except Exception as e:
                logger.error(f"[CHROMA] 컬렉션 {collection_name} 처리 중 오류 발생: {str(e)}")
                continue
                
        logger.info("[CHROMA] 모든 컬렉션 초기화 완료")
        
    except Exception as e:
        logger.error(f"[CHROMA] 컬렉션 초기화 중 오류 발생: {str(e)}")
        raise

def search_similar_in_collection(collection_name: str, query: str, top_k: int = 5) -> List[Document]:
    """
    [ChromaDB 컬렉션에서 유사 문서 검색]
    - 입력: 
        - collection_name: 검색할 컬렉션 이름
        - query: 검색 쿼리
        - top_k: 반환할 결과 수
    - 출력: 
        - 검색된 Document 리스트
    """
    try:
        # 1. 컬렉션 가져오기
        collection = client.get_collection(collection_name)
        
        # 2. 컬렉션 상태 로깅
        logger.info(f"[검색] 컬렉션: {collection_name}")
        current_model = collection.metadata.get('embedding_model')
        logger.info(f"[검색] 임베딩 모델: {current_model}")
        
        # 3. 컬렉션 데이터 확인
        count = collection.count()
        logger.info(f"[검색] 컬렉션 데이터 수: {count}")
        if count == 0:
            logger.warning(f"[검색] 컬렉션에 데이터가 없습니다: {collection_name}")
            return []
        
        # 4. 임베딩 차원 확인 및 검증
        collection_dimension = collection.metadata.get('hnsw:dimension', 384)
        
        # 5. 쿼리 임베딩 생성 (컬렉션의 모델 사용)
        query_embedding = get_hf_embedding(current_model).embed_query(query)
        logger.info(f"[검색] 쿼리 임베딩 차원: {len(query_embedding)}")
        
        # 5-1. 쿼리 임베딩 정상 여부 체크
        if any(np.isnan(x) for x in query_embedding):
            logger.error("[검색] 쿼리 임베딩에 nan 값 포함")
            return []
        if any(np.isinf(x) for x in query_embedding):
            logger.error("[검색] 쿼리 임베딩에 inf 값 포함")
            return []
        
        # 6. 임베딩 차원 검증
        if not validate_embedding_dimension(query_embedding, collection_dimension):
            logger.error(f"[검색] 임베딩 차원 불일치: 컬렉션({collection_dimension}) != 쿼리({len(query_embedding)})")
            return []
        
        # 7. 유사도 검색 (top_k를 2배로 늘려서 필터링 여유 확보)
        try:
            # 7-1. query_embeddings 방식으로 검색
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k * 2,
                include=["metadatas", "distances", "documents"]
            )
        except AttributeError:
            # 7-2. search 방식으로 검색 (이전 버전 호환)
            results = collection.search(
                query_embeddings=[query_embedding],
                n_results=top_k * 2,
                include=["metadatas", "distances", "documents"]
            )
        
        # 7-3. 검색 결과 정상 여부 체크
        if not results or not results.get('distances'):
            logger.error("[검색] 검색 결과 없음")
            return []
            
        # 7-4. 거리 값 정상 여부 체크
        distances = results['distances'][0]
        if any(np.isnan(d) for d in distances):
            logger.error("[검색] 검색 결과에 nan 거리 포함")
            return []
        if any(np.isinf(d) for d in distances):
            logger.error("[검색] 검색 결과에 inf 거리 포함")
            return []
        
        # 8. 검색 결과 로깅
        if results and results.get('documents'):
            logger.info(f"[검색] 검색 결과 수: {len(results['documents'][0])}")
            for i, doc in enumerate(results['documents'][0]):
                distance = results['distances'][0][i] if results['distances'] else float('inf')
                similarity = 1.0 - (distance / 2.0) if distance != float('inf') else 0.0
                logger.info(f"[검색] 결과 {i+1}: 유사도={similarity:.4f}, 거리={distance:.4f}")
        else:
            logger.warning("[검색] 검색 결과가 없습니다")
            return []
        
        # 9. 검색 결과를 Document로 변환 및 필터링
        documents = []
        if results and results.get('documents'):
            # 컬렉션의 임계값 가져오기 (기본값 0.7로 설정)
            logger.info(f"[검색] 컬렉션 임계값: {collection.metadata.get('similarity_threshold')}")
            logger.info(f"[검색] 컬렉션 임계값: {collection.metadata.get('similarity_threshold')}")
            logger.info(f"[검색] 컬렉션 임계값: {collection.metadata.get('similarity_threshold')}")
            
            collection_threshold = float(collection.metadata.get('similarity_threshold', 0.7))
            logger.info(f"[검색] 컬렉션 임계값: {collection_threshold}")
            
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                distance = results['distances'][0][i] if results['distances'] else float('inf')
                
                # 9-1. 기본 유사도 점수 계산 (거리를 유사도로 변환)
                similarity_score = 1.0 - (distance / 2.0) if distance != float('inf') else 0.0
                
                # 9-2. 검색 가중치 적용
                search_weight = metadata.get('search_weight', 0.5)
                weighted_score = similarity_score * search_weight
                
                # 9-3. 임계값 체크 (컬렉션의 임계값 사용)
                if similarity_score < collection_threshold:
                    logger.debug(f"[검색] 임계값 미달: {similarity_score:.4f} < {collection_threshold} (문서: {doc[:100]}...)")
                    continue
                
                # 9-4. Document 생성
                document = Document(
                    page_content=doc,
                    metadata={
                        **metadata,
                        'similarity_score': similarity_score,
                        'weighted_score': weighted_score,
                        'distance': distance,
                        'similarity_threshold': collection_threshold
                    }
                )
                documents.append(document)
                logger.info(f"[검색] 문서 추가됨: 유사도={similarity_score:.4f}, 내용={doc[:100]}...")
                
        logger.info(f"[검색] 최종 필터링된 문서 수: {len(documents)}")
        return documents
        
    except Exception as e:
        logger.error(f"[검색] 오류 발생: {str(e)}")
        return []

def validate_embedding_dimension(query_embedding: List[float], collection_dimension: int) -> bool:
    """
    임베딩 차원 검증
    
    Args:
        query_embedding: 쿼리 임베딩 벡터
        collection_dimension: 컬렉션의 임베딩 차원
        
    Returns:
        bool: 차원이 일치하면 True
    """
    if len(query_embedding) != collection_dimension:
        logger.error(f"[검증] 임베딩 차원 불일치: 쿼리({len(query_embedding)}) != 컬렉션({collection_dimension})")
        return False
    return True

def get_similar_context_from_chroma(query: str) -> str:
    """
    [ChromaDB에서 유사 문맥 검색]
    - 입력: 검색 쿼리
    - 출력: 검색된 문맥 문자열
    """
    try:
        logger.info(f"[문맥검색] 시작 - 쿼리: {query}")
        # 각 컬렉션에서 검색
        all_docs = []
        for collection in config.RAG_CHROMA_COLLECTIONS:
            docs = search_similar_in_collection(collection['collection'], query)
            if docs:  # 검색 결과가 있는 컬렉션만 로깅
                logger.info(f"[문맥검색] 컬렉션 {collection['collection']} 검색 결과: {len(docs)}개 문서")
                # 검색된 문서 상세 로깅
                for i, doc in enumerate(docs):
                    logger.info(f"[문맥검색] 문서 {i+1}:")
                    logger.info(f"[문맥검색] - 내용: {doc.page_content[:200]}...")
                    logger.info(f"[문맥검색] - 유사도: {doc.metadata.get('similarity_score', 'N/A')}")
                    logger.info(f"[문맥검색] - 메타데이터: {doc.metadata}")
            all_docs.extend(docs)
        
        # 검색 결과가 없으면 빈 문자열 반환
        if not all_docs:
            logger.warning("[문맥검색] 검색 결과 없음")
            return ""
        
        # 검색 결과를 문맥 문자열로 변환
        context = "\n\n".join([doc.page_content for doc in all_docs])
        logger.info(f"[문맥검색] 최종 문맥 생성 완료 (길이: {len(context)}자)")
        logger.info(f"[문맥검색] 총 {len(all_docs)}개 문서 사용")
        return f"\n참고 문맥:\n{context}"
    except Exception as e:
        logger.error(f"[문맥검색] 오류 발생: {str(e)}")
        return ""

def create_collection(collection_name: str, embedding_model: str) -> None:
    """
    [ChromaDB 컬렉션 생성]
    - 입력: 
        - collection_name: 생성할 컬렉션 이름
        - embedding_model: 사용할 임베딩 모델
    - 동작:
        - 컬렉션이 없으면 생성
        - 임베딩 모델 정보를 메타데이터에 저장
        - 임베딩 차원을 모델 정보에 따라 설정
    """
    try:
        # 임베딩 모델 초기화
        embeddings = get_hf_embedding(embedding_model)
        
        # 모델 정보 조회
        model_info = get_model_info(embedding_model)
        dimension = model_info["dimension"]
        
        # ChromaDB 클라이언트 초기화
        chroma_client = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=config.RAG_CHROMA_DIR
        )
        
        # 컬렉션 생성 (임베딩 차원을 모델 정보에 따라 설정)
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embeddings,
            metadata={
                "embedding_model": embedding_model,
                "embedding_dimension": dimension,
                "hnsw:dimension": dimension,
                "hnsw:space": "cosine",
                "hnsw:M": 16,
                "hnsw:construction_ef": 100,
                "hnsw:search_ef": 100
            }
        )
        
        logger.info(f"[컬렉션 생성] {collection_name} 컬렉션이 생성되었습니다.")
        logger.info(f"[컬렉션 생성] 임베딩 모델: {embedding_model}")
        logger.info(f"[컬렉션 생성] 임베딩 차원: {dimension}")
    except Exception as e:
        logger.error(f"ChromaDB 컬렉션 생성 중 오류 발생: {str(e)}")
        raise 