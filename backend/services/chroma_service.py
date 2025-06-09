# backend/services/chroma_service.py

# 한글 주석 포함
from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from tqdm import tqdm  # 진행률 표시를 위한 tqdm 추가
from config import Config  # 공통 설정 import

def initialize_chroma_from_docx(docx_path=None, chroma_dir=None, collection_name="policy_collection"):
    """
    워드(docx) 파일을 읽어 문단별로 임베딩 후 Chroma DB에 저장합니다.
    chroma_dir와 docx_path는 config.py의 Config에서 기본값을 가져옵니다.
    tqdm으로 진행률을 표시합니다.
    """
    # 경로 기본값 설정
    if docx_path is None:
        docx_path = Config.POLICY_DOCX_PATH
    if chroma_dir is None:
        chroma_dir = Config.CHROMA_DB_DIR

    # 워드 파일에서 텍스트 추출
    doc = Document(docx_path)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    if not paragraphs:
        print("문서에 저장할 문단이 없습니다.")
        return

    # 임베딩 모델 로드
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(paragraphs).tolist()

    # Chroma DB 인스턴스 생성 (경로 변경)
    client = chromadb.Client(Settings(persist_directory=chroma_dir))
    collection = client.get_or_create_collection(collection_name)

    # 기존 데이터 삭제(초기화 목적)
    all_ids = collection.get()['ids']
    if all_ids:
        collection.delete(ids=all_ids)  # 전체 데이터 안전 삭제

    # tqdm으로 진행률 표시하며 문단별로 벡터와 메타데이터 저장
    for idx, (text, embedding) in tqdm(enumerate(zip(paragraphs, embeddings)), total=len(paragraphs), desc="Chroma 저장 진행"):
        collection.add(
            ids=[f"para_{idx}"],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "source": os.path.basename(docx_path),
                "paragraph_index": idx
            }]
        )
    print(f"Chroma DB에 {len(paragraphs)}개 문단 저장 완료.")

def get_similar_context_from_chroma(query, chroma_dir=None, collection_name="policy_collection", top_k=3):
    """
    Chroma DB에서 질문(query)과 유사한 정책/가이드 문단을 top_k개 검색하여 텍스트로 반환합니다.
    chroma_dir는 config.py의 기본값을 사용합니다.
    """
    if chroma_dir is None:
        from config import Config
        chroma_dir = Config.CHROMA_DB_DIR
    client = chromadb.Client(Settings(persist_directory=chroma_dir))
    collection = client.get_or_create_collection(collection_name)
    # 임베딩 모델 로드 (최적화 위해 전역화 가능)
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    # 검색된 문단을 한글 주석과 함께 텍스트로 합침
    context_list = results.get('documents', [[]])[0]
    context_text = '\n'.join(context_list)
    return context_text 