from flask import Blueprint, request, jsonify, g
from services.auth_service import authenticate_user, create_jwt_token, decode_jwt_token, log_login_history
from common.response import ApiResponse
import os
import logging
from functools import wraps

# 로거 설정
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# JWT 인증 데코레이터 (먼저 정의)
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.info(f"[JWT] 인증 데코레이터 시작")
        
        auth_header = request.headers.get('Authorization', None)
        logger.info(f"[JWT] Authorization 헤더: {auth_header}")
        
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning(f"[JWT] Authorization 헤더가 없거나 Bearer 형식이 아님")
            return ApiResponse.error(code="AUTH_TOKEN_REQUIRED", message='인증 토큰이 필요합니다.', status=401)
        
        token = auth_header.split(' ')[1]
        logger.info(f"[JWT] 추출된 토큰: {token[:20]}...")
        
        payload = decode_jwt_token(token)
        if not payload:
            logger.warning(f"[JWT] 토큰 검증 실패")
            return ApiResponse.error(code="AUTH_TOKEN_INVALID", message='유효하지 않거나 만료된 토큰입니다.', status=401)
        
        logger.info(f"[JWT] 토큰 검증 성공, 사용자: {payload.get('email')}")
        g.user = payload
        return f(*args, **kwargs)
    return decorated

# 로그인 엔드포인트
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    user = authenticate_user(email, password)
    if not user:
        # 로그인 실패 시에도 이력 기록 (user_id는 None)
        log_login_history(None, False, ip, user_agent)
        # 로그인 실패 시, code와 message 순서에 맞게 전달
        return ApiResponse.error(code="AUTH_INVALID_CREDENTIALS", message='이메일 또는 비밀번호가 올바르지 않습니다.', status=401)

    # 로그인 성공 이력 기록
    log_login_history(user['id'], True, ip, user_agent)
    
    # 직원 정보 추출
    employee_info = None
    if user and user.get('employee_id'):
        employee_info = {
            'employee_id': user['employee_id'],
            'employee_name': user.get('employee_name'),
            'employee_position': user.get('employee_position'),
            'employee_dept': user.get('employee_dept'),
            'employee_email': user.get('employee_email'),
            'employee_phone': user.get('employee_phone')
        }
    
    token = create_jwt_token(user['id'], user['email'], user['role'], user['name'], employee_info)
    return ApiResponse.success({
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'role': user['role'],
            'employee_id': user['employee_id'],
            'employee_name': user.get('employee_name'),
            'employee_position': user.get('employee_position'),
            'employee_dept': user.get('employee_dept'),
            'employee_email': user.get('employee_email'),
            'employee_phone': user.get('employee_phone')
        }
    })

# 토큰 갱신 엔드포인트
@auth_bp.route('/api/auth/refresh', methods=['POST'])
@jwt_required
def refresh_token():
    """JWT 토큰을 갱신합니다."""
    try:
        logger.info(f"[AUTH] 토큰 갱신 요청: {g.user.get('email')}")
        
        # 현재 사용자 정보로 새 토큰 생성
        # JWT 토큰에서 직원 정보 추출
        employee_info = None
        if g.user.get('employee_id'):
            employee_info = {
                'employee_id': g.user.get('employee_id'),
                'employee_name': g.user.get('employee_name'),
                'employee_position': g.user.get('employee_position'),
                'employee_dept': g.user.get('employee_dept'),
                'employee_email': g.user.get('employee_email'),
                'employee_phone': g.user.get('employee_phone')
            }
        
        new_token = create_jwt_token(
            g.user['user_id'], 
            g.user['email'], 
            g.user['role'],
            g.user.get('name'),
            employee_info
        )
        
        logger.info(f"[AUTH] 토큰 갱신 완료: {g.user.get('email')}")
        return ApiResponse.success({
            'token': new_token,
            'message': '토큰이 성공적으로 갱신되었습니다.'
        })
        
    except Exception as e:
        logger.error(f"[AUTH] 토큰 갱신 실패: {str(e)}")
        return ApiResponse.error(
            code="AUTH_REFRESH_FAILED", 
            message='토큰 갱신에 실패했습니다.', 
            status=500
        )

# 내 정보 조회
@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required
def me():
    user = g.user
    return ApiResponse.success({
        'user_id': user['user_id'],
        'email': user['email'],
        'role': user['role']
    }) 