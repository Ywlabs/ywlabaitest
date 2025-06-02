import pymysql
import os
from dotenv import load_dotenv

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
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # schema.sql 파일 읽기
        with open('schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # SQL 문을 세미콜론(;)으로 분리
        sql_statements = sql_script.split(';')
        
        # 각 SQL 문 실행
        for statement in sql_statements:
            # 빈 문장이나 주석만 있는 경우 스킵
            if statement.strip() and not statement.strip().startswith('--'):
                cur.execute(statement)
        
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close() 