# OpenAI 임베딩 관련 함수/클래스는 이 파일에 구현하세요.

from langchain_community.embeddings import OpenAIEmbeddings

# OpenAI 임베딩 객체 반환 함수

def get_openai_embedding(openai_api_key=None, model_name="text-embedding-ada-002"):
    """OpenAI 임베딩 객체 반환"""
    return OpenAIEmbeddings(openai_api_key=openai_api_key, model=model_name) 