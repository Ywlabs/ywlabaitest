from flask import Blueprint, request, jsonify
from services.chat_service import get_chat_history, get_popular_questions, save_chat_interaction, get_ai_response
from common.logger import setup_logger
from database import get_db_connection
import re
from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
from flask import current_app


chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')
logger = setup_logger('chat_routes')

routes_bp = Blueprint('routes', __name__, url_prefix='/api')

@chat_bp.route('', methods=['POST'], strict_slashes=False)
@chat_bp.route('/', methods=['POST'], strict_slashes=False)
def chat():
    """채팅 메시지 처리"""
    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'message': '메시지가 필요합니다.'
            }), 400
        
        # 1. 벡터 검색으로 유사한 질문 찾기
        # (ChromaDB 기반으로 chat_service 내부에서 처리)
        similar_question = None
        # AI 응답 생성 (DB 우선, 없으면 LLM)
        response, similar_question = get_ai_response(user_message, similar_question)

        # 2. 대화 기록 저장
        intent_tag = similar_question['intent_tag'] if similar_question and 'intent_tag' in similar_question else None
        save_chat_interaction(
            user_message,
            response['data']['response'],
            intent_tag,
            response['data']['route_code'],
            response.get('data', {}).get('response_type', 'db'),  # response_source
            response.get('data', {}).get('response_time', None),  # response_time
            response  # 전체 응답 JSON 저장
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'서버 오류가 발생했습니다. (에러: {str(e)})'
        }), 500

@chat_bp.route('/history', methods=['GET'])
def chat_history():
    """채팅 히스토리 조회"""
    try:
        logger.info("채팅 히스토리 조회 시작")
        history = get_chat_history()
        logger.info(f"채팅 히스토리 조회 완료: {len(history)}개 항목")
        return jsonify({
            'status': 'success',
            'data': history
        })
    except Exception as e:
        logger.error(f"Error in chat history endpoint: {str(e)}", exc_info=True)  # 스택 트레이스 포함
        return jsonify({
            'status': 'error',
            'message': f'채팅 히스토리를 불러오는데 실패했습니다. (에러: {str(e)})'
        }), 500

@chat_bp.route('/popular', methods=['GET'])
def popular_questions():
    """인기 질문 목록 조회"""
    questions = get_popular_questions()
    return jsonify(questions)

@routes_bp.route('/routes', methods=['GET'])
def get_routes():
    """routes 테이블 전체 정보 반환"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT route_code, route_type, route_name, route_path FROM routes')
            routes = cursor.fetchall()
        return jsonify({'status': 'success', 'data': routes})
    finally:
        conn.close() 