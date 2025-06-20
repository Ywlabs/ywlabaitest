import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from database import get_db_connection
from flask import current_app
from config import config
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# 환경변수에서 JWT 시크릿/만료시간 로드
JWT_SECRET = config.JWT_SECRET
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_MINUTES = config.JWT_EXPIRE_MINUTES

# 비밀번호 해시 생성 함수
def hash_password(password):
    """비밀번호를 bcrypt로 해시화합니다."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# 비밀번호 검증 함수 (bcrypt)
def verify_password(plain_password, hashed_password):
    """평문 비밀번호와 해시값을 비교합니다."""
    logger.info(f"[AUTH] 비밀번호 검증 시작")
    logger.info(f"[AUTH] 입력된 비밀번호: {plain_password}")
    logger.info(f"[AUTH] DB 해시값 타입: {type(hashed_password)}")
    logger.info(f"[AUTH] DB 해시값: {hashed_password}")
    
    try:
        # 해시값이 None이거나 빈 문자열인 경우
        if not hashed_password:
            logger.warning(f"[AUTH] 해시값이 None이거나 빈 문자열입니다")
            return False
        
        # 평문 비밀번호를 bytes로 변환
        plain_bytes = plain_password.encode('utf-8')
        logger.info(f"[AUTH] 평문 비밀번호를 bytes로 변환했습니다")
        
        # 해시값 처리 - bcrypt.checkpw는 bytes를 요구함
        if isinstance(hashed_password, bytes):
            # 이미 bytes인 경우
            hash_bytes = hashed_password
            logger.info(f"[AUTH] 해시값이 이미 bytes 타입입니다")
        elif isinstance(hashed_password, str):
            # 문자열인 경우 - bytes로 변환
            hash_bytes = hashed_password.encode('utf-8')
            logger.info(f"[AUTH] 문자열 해시값을 bytes로 변환했습니다")
        else:
            logger.error(f"[AUTH] 지원하지 않는 해시값 타입: {type(hashed_password)}")
            return False
        
        # bcrypt로 검증
        result = bcrypt.checkpw(plain_bytes, hash_bytes)
        logger.info(f"[AUTH] bcrypt 검증 결과: {result}")
        return result
    except Exception as e:
        # 검증 중 오류 발생 시 False 반환
        logger.error(f"[AUTH] 비밀번호 검증 오류: {e}")
        logger.error(f"[AUTH] 오류 상세: {type(e).__name__}: {str(e)}")
        return False

# JWT 토큰 생성 함수
def create_jwt_token(user_id, email, role, name=None, employee_info=None):
    """JWT 액세스 토큰을 생성합니다."""
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'name': name,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    
    # 직원 정보가 있으면 토큰에 포함
    if employee_info:
        payload.update({
            'employee_id': employee_info.get('employee_id'),
            'employee_name': employee_info.get('employee_name'),
            'employee_position': employee_info.get('employee_position'),
            'employee_dept': employee_info.get('employee_dept'),
            'employee_email': employee_info.get('employee_email'),
            'employee_phone': employee_info.get('employee_phone')
        })
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# JWT 토큰 검증 함수
def decode_jwt_token(token):
    """JWT 토큰을 검증하고 payload를 반환합니다."""
    logger.info(f"[AUTH] JWT 토큰 검증 시작")
    logger.info(f"[AUTH] 토큰: {token[:20]}...")  # 토큰의 앞 20자만 로그
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        logger.info(f"[AUTH] JWT 토큰 검증 성공: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning(f"[AUTH] JWT 토큰 만료됨")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"[AUTH] JWT 토큰 검증 실패: {e}")
        return None
    except Exception as e:
        logger.error(f"[AUTH] JWT 토큰 검증 중 예상치 못한 오류: {e}")
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
    logger.info(f"[AUTH] 사용자 인증 시작 - 이메일: {email}")
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT u.id, u.email, u.password_hash, u.name, u.role, u.is_active, u.employee_id,
                   e.name as employee_name, e.position, e.dept_nm, e.email as employee_email, e.phone
            FROM users u
            LEFT JOIN employees e ON u.employee_id = e.id
            WHERE u.email=%s
            """,
            (email,)
        )
        row = cursor.fetchone()
    conn.close()
    
    if not row:
        logger.warning(f"[AUTH] 사용자를 찾을 수 없습니다: {email}")
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
            'employee_id': row['employee_id'],
            'employee_name': row['employee_name'],
            'employee_position': row['position'],
            'employee_dept': row['dept_nm'],
            'employee_email': row['employee_email'],
            'employee_phone': row['phone']
        }
    else:
        user = {
            'id': row[0],
            'email': row[1],
            'password_hash': row[2],
            'name': row[3],
            'role': row[4],
            'is_active': row[5],
            'employee_id': row[6],
            'employee_name': row[7],
            'employee_position': row[8],
            'employee_dept': row[9],
            'employee_email': row[10],
            'employee_phone': row[11]
        }
    
    logger.info(f"[AUTH] 사용자 정보 조회 완료: {user['email']}, 활성화: {user['is_active']}")
    logger.info(f"[AUTH] 사용자 비밀번호 해시: {user['password_hash']}")
    logger.info(f"[AUTH] 직원 정보: employee_id={user['employee_id']}, employee_name={user['employee_name']}, position={user['employee_position']}")
    
    if not user['is_active']:
        logger.warning(f"[AUTH] 비활성화된 사용자입니다: {email}")
        return None
    
    if not verify_password(password, user['password_hash']):
        logger.warning(f"[AUTH] 비밀번호 검증 실패: {email}")
        return None
    
    logger.info(f"[AUTH] 사용자 인증 성공: {email}")
    return user

# 사용자 비밀번호 업데이트 함수
def update_user_password(email, new_password):
    """사용자의 비밀번호를 새로운 해시로 업데이트합니다."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 새로운 해시 생성
            new_hash = hash_password(new_password)
            logger.info(f"[AUTH] 새로운 해시 생성: {new_hash}")
            
            # 비밀번호 업데이트
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE email = %s",
                (new_hash, email)
            )
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"[AUTH] 사용자 {email}의 비밀번호가 업데이트되었습니다.")
                return True
            else:
                logger.warning(f"[AUTH] 사용자 {email}를 찾을 수 없습니다.")
                return False
    except Exception as e:
        logger.error(f"[AUTH] 비밀번호 업데이트 오류: {e}")
        return False
    finally:
        conn.close() 