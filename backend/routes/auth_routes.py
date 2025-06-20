from flask import Blueprint, request, jsonify, g
from services.auth_service import authenticate_user, create_jwt_token, decode_jwt_token, log_login_history
from common.response import ApiResponse
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 로그인 엔드포인트
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    user = authenticate_user(email, password)
    if not user:
        # 로그인 실패 시, code와 message 순서에 맞게 전달
        return ApiResponse.error(code="AUTH_INVALID_CREDENTIALS", message='이메일 또는 비밀번호가 올바르지 않습니다.', status=401)

    # 로그인 성공 이력 기록
    log_login_history(user['id'], True, ip, user_agent)
    token = create_jwt_token(user['id'], user['email'], user['role'])
    return ApiResponse.success({
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'role': user['role'],
            'employee_id': user['employee_id']
        }
    })

# JWT 인증 데코레이터
from functools import wraps

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return ApiResponse.error(code="AUTH_TOKEN_REQUIRED", message='인증 토큰이 필요합니다.', status=401)
        token = auth_header.split(' ')[1]
        payload = decode_jwt_token(token)
        if not payload:
            return ApiResponse.error(code="AUTH_TOKEN_INVALID", message='유효하지 않거나 만료된 토큰입니다.', status=401)
        g.user = payload
        return f(*args, **kwargs)
    return decorated

# 내 정보 조회
@auth_bp.route('/me', methods=['GET'])
@jwt_required
def me():
    user = g.user
    return ApiResponse.success({
        'user_id': user['user_id'],
        'email': user['email'],
        'role': user['role']
    }) 