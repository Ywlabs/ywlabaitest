import os
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()

class BaseConfig:
    """기본 설정 클래스"""
    def __init__(self):
        # 환경 변수에서 현재 프로파일 가져오기
        self.profile = os.getenv('APP_PROFILE', 'dev')
        
        # function_mapping.json 로드
        config_path = Path(__file__).parent / 'core' / 'profiles' / 'function_mapping.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            self.function_mappings = json.load(f)

        # RAG용 ChromaDB 및 컬렉션별 설정
        self.RAG_CHROMA_DIR = os.path.join(os.path.dirname(__file__), 'chromadb', 'rag_db')
        self.RAG_CHROMA_COLLECTIONS = [
            {
                "path": "./metadata/docx/ywlabs_policy_20250609.docx",
                "collection": "policy_collection",
                "type": "docx",
                "embedding_model": "snunlp/KR-SBERT-V40K-klueNLI-augSTS",
                "parser": "docx",
                "search_top_k": 5,
                "similarity_threshold": 0.6,  # 정책 문서는 높은 정확도 필요
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 200,  # 정책 문서는 더 정확한 검색 필요
                "hnsw:search_ef": 200,
                "hnsw:M": 32
            },
        ]

        # DB 기반 컬렉션 분리 관리
        self.DB_CHROMA_COLLECTIONS = [
            {
                "collection": "widget_collection",
                "type": "widget",
                "parser": "database",
                "embedding_model": "snunlp/KR-SBERT-V40K-klueNLI-augSTS",
                "get_all_func": "services.widget_service.get_all_widgets",
                "to_doc_func": "core.converters.widget_converter.widget_to_document",
                "search_top_k": 10,
                "similarity_threshold": 0.8,  # 위젯은 더 유연한 매칭 허용
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 100,
                "hnsw:search_ef": 100,
                "hnsw:M": 16
            },
            {
                "collection": "chatbot_collection",
                "type": "pattern",
                "parser": "database",
                "embedding_model": "snunlp/KR-SBERT-V40K-klueNLI-augSTS",
                "get_all_func": "services.pattern_service.get_all_patterns",
                "to_doc_func": "core.converters.pattern_converter.pattern_to_document",
                "search_top_k": 5,
                "similarity_threshold": 0.8,  # 챗봇 패턴은 높은 정확도 필요
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 200,  # 챗봇은 더 정확한 검색 필요
                "hnsw:search_ef": 200,
                "hnsw:M": 32
            },
        ]

class DevConfig(BaseConfig):
    """개발 환경 설정"""
    def __init__(self):
        super().__init__()
        # Flask 설정
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
        
        # MySQL 설정
        self.MYSQL_HOST = os.getenv('DB_HOST', '192.168.0.200')
        self.MYSQL_USER = os.getenv('DB_USER', 'ywlabsdev')
        self.MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'ywlabs#20151010Q')
        self.MYSQL_DB = os.getenv('DB_NAME', 'ywlabtest')
        self.MYSQL_PORT = int(os.getenv('DB_PORT', 3307))
        
        # SQLAlchemy 설정
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        # OpenAI API 설정
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        
        # 기타 설정
        self.DEBUG = True
        self.LOG_LEVEL = 'DEBUG'

class ProdConfig(BaseConfig):
    """운영 환경 설정"""
    def __init__(self):
        super().__init__()
        # Flask 설정
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        
        # MySQL 설정
        self.MYSQL_HOST = os.getenv('DB_HOST', '192.168.0.200')
        self.MYSQL_USER = os.getenv('DB_USER', 'ywlabsdev')
        self.MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'ywlabs#20151010Q')
        self.MYSQL_DB = os.getenv('DB_NAME', 'ywlabtest')
        self.MYSQL_PORT = int(os.getenv('DB_PORT', 3307))
        
        # SQLAlchemy 설정
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        # OpenAI API 설정
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        
        # 기타 설정
        self.DEBUG = False
        self.LOG_LEVEL = 'INFO'

class TestConfig(BaseConfig):
    """테스트 환경 설정"""
    def __init__(self):
        super().__init__()
        # Flask 설정
        self.SECRET_KEY = 'test'
        
        # MySQL 설정
        self.MYSQL_HOST = os.getenv('DB_HOST', '192.168.0.200')
        self.MYSQL_USER = os.getenv('DB_USER', 'ywlabsdev')
        self.MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'ywlabs#20151010Q')
        self.MYSQL_DB = os.getenv('DB_NAME', 'ywlabtest')
        self.MYSQL_PORT = int(os.getenv('DB_PORT', 3307))
        
        # SQLAlchemy 설정
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        # OpenAI API 설정
        self.OPENAI_API_KEY = 'test_key'
        
        # 기타 설정
        self.DEBUG = True
        self.LOG_LEVEL = 'DEBUG'

        # 테스트 환경에서만 ChromaDB 디렉토리 변경
        self.RAG_CHROMA_DIR = './chromadb/test_rag_db'

def get_config():
    """환경별 설정 인스턴스 반환"""
    profile = os.getenv('APP_PROFILE', 'dev')
    config_map = {
        'dev': DevConfig,
        'prod': ProdConfig,
        'test': TestConfig
    }
    return config_map[profile]()

# 전역 설정 인스턴스
config = get_config() 