import pymysql
import os
from dotenv import load_dotenv
import logging

# 로거 설정
logger = logging.getLogger(__name__)

load_dotenv()

def get_db_connection():
    """데이터베이스 연결"""
    return pymysql.connect(
        host=os.getenv('DB_HOST', '192.168.0.200'),
        user=os.getenv('DB_USER', 'ywlabsdev'),
        password=os.getenv('DB_PASSWORD', 'ywlabs#20151010Q'),
        database=os.getenv('DB_NAME', 'ywlabtest'),
        port=3307,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    """데이터베이스 초기화"""
    try:
        connection = get_db_connection()
        if connection:
            logger.info("[DB] 데이터베이스 연결 성공")
            connection.close()
    except Exception as e:
        logger.error(f"[DB] 초기화 중 오류 발생: {str(e)}")
        raise
