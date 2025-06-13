# HuggingFace 임베딩 관련 함수/클래스는 이 파일에 구현하세요.

from langchain_huggingface import HuggingFaceEmbeddings

# HuggingFace 임베딩 객체 반환 함수

def get_hf_embedding(model_name):
    """HuggingFace 임베딩 객체 반환"""
    return HuggingFaceEmbeddings(model_name=model_name) 