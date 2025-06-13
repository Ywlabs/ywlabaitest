import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # MySQL 설정
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'ywlabs')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
    # SQLAlchemy 설정
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI API 설정
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # 기타 설정
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # RAG용 ChromaDB 및 컬렉션별 설정 (문서/이미지/옵션 포함)
    RAG_CHROMA_DIR = './chromadb/rag_db'
    RAG_CHROMA_COLLECTIONS = [
        {
            "path": "./metadata/docx/ywlabs_policy_20250609.docx",
            "collection": "policy_collection",
            "type": "docx",
            "embedding_model": "jhgan/ko-sroberta-multitask",
            "parser": "docx",
            "search_top_k": 5
        },
    ]

    # DB 기반 컬렉션 분리 관리
    DB_CHROMA_COLLECTIONS = [
        {
            "collection": "widget",
            "type": "widget",
            "parser": "database",
            "embedding_model": "jhgan/ko-sroberta-multitask",
            "get_all_func": "services.widget_service.get_all_widgets",
            "to_doc_func": "core.converters.widget_converter.widget_to_document",
            "search_top_k": 10
        },
        # 챗봇 패턴/응답용 컬렉션 추가
        {
            "collection": "chatbot",
            "type": "pattern",
            "parser": "database",
            "embedding_model": "jhgan/ko-sroberta-multitask",
            "get_all_func": "services.pattern_service.get_all_patterns",
            "to_doc_func": "services.pattern_service.pattern_to_document",
            "search_top_k": 5
        },
    ] 