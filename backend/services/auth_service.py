import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from database import get_db_connection
from flask import current_app
from config import config

# 환경변수에서 JWT 시크릿/만료시간 로드
JWT_SECRET = config.JWT_SECRET
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_MINUTES = config.JWT_EXPIRE_MINUTES

# 비밀번호 검증 함수 (bcrypt)
def verify_password(plain_password, hashed_password):
    """평문 비밀번호와 해시값을 비교합니다."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWT 토큰 생성 함수
def create_jwt_token(user_id, email, role):
    """JWT 액세스 토큰을 생성합니다."""
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# JWT 토큰 검증 함수
def decode_jwt_token(token):
    """JWT 토큰을 검증하고 payload를 반환합니다."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# 로그인 이력 기록 함수
def log_login_history(user_id, success, ip_address=None, user_agent=None):
    """로그인 시도 이력을 기록합니다."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO login_history (user_id, success, ip_address, user_agent)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, success, ip_address, user_agent)
        )
    conn.commit()
    conn.close()

# 사용자 인증 함수
def authenticate_user(email, password):
    """이메일/비밀번호로 사용자 인증. 성공 시 사용자 dict 반환, 실패 시 None."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, password_hash, name, role, is_active, employee_id
            FROM users WHERE email=%s
            """,
            (email,)
        )
        row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    # row가 dict인지 tuple인지 자동 분기
    if isinstance(row, dict):
        user = {
            'id': row['id'],
            'email': row['email'],
            'password_hash': row['password_hash'],
            'name': row['name'],
            'role': row['role'],
            'is_active': row['is_active'],
            'employee_id': row['employee_id']
        }
    else:
        user = {
            'id': row[0],
            'email': row[1],
            'password_hash': row[2],
            'name': row[3],
            'role': row[4],
            'is_active': row[5],
            'employee_id': row[6]
        }
    if not user['is_active']:
        return None
    if not verify_password(password, user['password_hash']):
        return None
    return user 