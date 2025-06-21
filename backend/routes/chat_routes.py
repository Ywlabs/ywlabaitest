from flask import Blueprint, request, g
from services.chat_service import get_chat_history, get_popular_questions, save_chat_interaction, get_ai_response, migrate_chat_history_user_id
from common.logger import setup_logger
from database import get_db_connection
import re
from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
from flask import current_app
from common.response import ApiResponse
from routes import jwt_required  # JWT 인증 데코레이터 import

# 로거 설정
logger = setup_logger('chat_routes')

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'], strict_slashes=False)
@jwt_required  # JWT 인증 필요
def chat():
    """
    챗봇 메시지 처리
    """
    try:
        data = request.get_json()
        user_message = data.get('message')
        chat_history = data.get('chat_history', [])
        
        if not user_message:
            return ApiResponse.error("ERR_NO_MESSAGE", "메시지가 필요합니다.", reason="message 파라미터 없음", status=400)
        
        # JWT 토큰에서 사용자 ID 가져오기
        user_id = g.user.get('user_id')
        logger.info(f"[CHAT] 챗봇 요청 - 사용자: {user_id}, 메시지: {user_message[:50]}...")
        
        response = get_ai_response(user_message, chat_history)
        save_chat_interaction(
            user_message,
            response.get('response', '응답을 생성할 수 없습니다.'),
            response.get('pattern_type'),
            response.get('route_code'),
            response.get('response_type'),
            None,
            response,
            user_id  # 사용자 ID 추가
        )
        return ApiResponse.success(data=response, message="AI 응답 생성 성공")
    except Exception as e:
        logger.error(f"챗봇 응답 생성 중 오류 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "서버 오류가 발생했습니다.", reason=str(e), status=500)

@chat_bp.route('/api/chat/history', methods=['GET'])
@jwt_required  # JWT 인증 필요
def chat_history():
    """
    챗봇 히스토리 조회 (모든 사용자는 자신의 히스토리만, 최근 20건)
    """
    try:
        # JWT 토큰에서 사용자 ID 가져오기
        user_id = g.user.get('user_id')
        
        logger.info(f"챗봇 히스토리 조회 - 사용자: {user_id}")
        history = get_chat_history(user_id, limit=20)  # 최근 20건만 조회
        
        logger.info(f"챗봇 히스토리 조회 완료: {len(history)}개 항목 (사용자: {user_id})")
        return ApiResponse.success(data=history, message="챗봇 히스토리 조회 성공")
    except Exception as e:
        logger.error(f"챗봇 히스토리 조회 중 오류 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "챗봇 히스토리 조회 실패", reason=str(e), status=500)

@chat_bp.route('/api/chat/popular', methods=['GET'])
@jwt_required  # JWT 인증 필요
def popular_questions():
    """
    인기 질문 목록 조회
    """
    try:
        questions = get_popular_questions()
        return ApiResponse.success(data=questions, message="인기 질문 조회 성공")
    except Exception as e:
        logger.error(f"인기 질문 조회 중 오류 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "인기 질문 조회 실패", reason=str(e), status=500)

@chat_bp.route('/api/chat/migrate', methods=['POST'])
@jwt_required  # JWT 인증 필요
def migrate_chat_history():
    """
    챗봇 히스토리 마이그레이션 (관리자만)
    """
    try:
        # JWT 토큰에서 사용자 역할 확인
        user_role = g.user.get('role')
        user_id = g.user.get('user_id')
        
        if user_role != 'admin':
            logger.warning(f"권한 없음 - 마이그레이션 시도: 사용자 {user_id}, 역할 {user_role}")
            return ApiResponse.error("ERR_PERMISSION", "관리자 권한이 필요합니다.", status=403)
        
        logger.info(f"챗봇 히스토리 마이그레이션 시작 - 관리자: {user_id}")
        migrate_chat_history_user_id()
        
        return ApiResponse.success(message="챗봇 히스토리 마이그레이션이 완료되었습니다.")
    except Exception as e:
        logger.error(f"챗봇 히스토리 마이그레이션 중 오류 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "마이그레이션 실패", reason=str(e), status=500) 