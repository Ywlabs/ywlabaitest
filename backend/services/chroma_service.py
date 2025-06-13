# backend/services/chroma_service.py

# 한글 주석 포함
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document as LC_Document
from docx import Document as DocxDocument
from config import Config
import os
from tqdm import tqdm  # 진행률 표시를 위한 tqdm 추가
import glob
import importlib
from core.embeddings.hf_embedding import get_hf_embedding

def initialize_rag_collections():
    """
    Config.RAG_CHROMA_COLLECTIONS 기반으로 여러 문서/이미지/컬렉션을 일괄 초기화
    (docx, pdf, image, 등 타입별 파서/임베딩/저장 구조)
    glob 패턴이 path에 들어오면 모든 파일을 반복 처리
    """
    for item in Config.RAG_CHROMA_COLLECTIONS:
        print(f"\n[초기화] {item['collection']} ({item['type']}) - {item['path']}")
        docs = []
        # 1. 파싱
        if item["parser"] == "docx":
            file_list = glob.glob(item["path"])
            for file_path in file_list:
                docx = DocxDocument(file_path)
                paragraphs = [para.text.strip() for para in docx.paragraphs if para.text.strip()]
                docs.extend([
                    LC_Document(
                        page_content=para,
                        metadata={
                            "source": os.path.basename(file_path),
                "paragraph_index": idx
                        }
                    )
                    for idx, para in enumerate(paragraphs)
                ])
        elif item["parser"] == "pdf":
            # TODO: PDF 파싱 구현 필요 (예: PyPDF2 등)
            print("PDF 파싱은 아직 미구현입니다.")
            docs = []
        elif item["parser"] == "image_ocr":
            # TODO: 이미지 OCR 파싱 구현 필요 (예: pytesseract 등)
            print("이미지 OCR 파싱은 아직 미구현입니다.")
            docs = []
        else:
            print(f"알 수 없는 parser: {item['parser']}")
            docs = []
        if not docs:
            print("저장할 문서가 없습니다.")
            continue
        # 2. 임베딩 모델
        embeddings = get_hf_embedding(item["embedding_model"])
        # 3. Chroma 컬렉션에 저장
        vector_store = Chroma(
            persist_directory=Config.RAG_CHROMA_DIR,
            collection_name=item["collection"],
            embedding_function=embeddings
        )
        vector_store.add_documents(docs)
        print(f"✓ {item['collection']}에 {len(docs)}개 문서/문단 임베딩 저장 완료.")

# DB 기반 컬렉션 초기화 함수
def get_func_from_str(func_path):
    """
    'services.widget_service.get_all_widgets' → 실제 함수 객체 반환
    """
    module_path, func_name = func_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)

def initialize_db_collections():
    """
    Config.DB_CHROMA_COLLECTIONS 기반으로 DB 컬렉션별 임베딩 일괄 저장
    """
    for item in Config.DB_CHROMA_COLLECTIONS:
        print(f"\n[DB초기화] {item['collection']} ({item['type']})")
        get_all_func = get_func_from_str(item["get_all_func"])
        to_doc_func = get_func_from_str(item["to_doc_func"])
        records = get_all_func()
        docs = [to_doc_func(r) for r in records]
        if not docs:
            print("저장할 문서가 없습니다.")
            continue
        embeddings = get_hf_embedding(item["embedding_model"])
        vector_store = Chroma(
            persist_directory=Config.RAG_CHROMA_DIR,
            collection_name=item["collection"],
            embedding_function=embeddings
        )
        vector_store.add_documents(docs)
        print(f"✓ {item['collection']}에 {len(docs)}개 DB 임베딩 저장 완료.")

def search_similar_in_collection(collection_name: str, query: str, top_k: int = 10):
    """
    DB_CHROMA_COLLECTIONS의 지정 컬렉션에서 쿼리로 유사 문서 검색
    """
    # config에서 해당 컬렉션 정보 찾기
    item = next((c for c in Config.DB_CHROMA_COLLECTIONS if c["collection"] == collection_name), None)
    if not item:
        print(f"[search_similar_in_collection] 컬렉션 {collection_name} 설정을 찾을 수 없습니다.")
        return []
    embeddings = get_hf_embedding(item["embedding_model"])
    vector_store = Chroma(
        persist_directory=Config.RAG_CHROMA_DIR,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    docs = vector_store.similarity_search(query, k=top_k)
    # 검색된 문서의 metadata 전체를 로그로 출력
    for idx, doc in enumerate(docs):
        print(f"[ChromaDB 검색결과] #{idx+1} metadata: {doc.metadata}")
    return docs

def get_similar_context_from_chroma(query: str, top_k: int = 3):
    """
    RAG_CHROMA_COLLECTIONS에 정의된 모든 컬렉션에서 쿼리로 유사 문단/문서(top_k개)를 찾아 리스트로 반환
    (문서/이미지 등 비정형 데이터 RAG 컨텍스트 전용)
    """
    results = []
    for item in Config.RAG_CHROMA_COLLECTIONS:
        embeddings = get_hf_embedding(item["embedding_model"])
        vector_store = Chroma(
            persist_directory=Config.RAG_CHROMA_DIR,
            collection_name=item["collection"],
            embedding_function=embeddings
        )
        docs = vector_store.similarity_search(query, k=top_k)
        results.extend(docs)
    return results 