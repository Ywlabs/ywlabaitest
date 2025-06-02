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