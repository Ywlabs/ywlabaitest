from flask import Blueprint, request, jsonify
from services.chat_service import get_chat_history, get_popular_questions, save_chat_interaction, get_ai_response
from common.logger import setup_logger
from database import get_db_connection
import re
from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
from flask import current_app

# 로거 설정
logger = setup_logger('chat_routes')

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'], strict_slashes=False)
def chat():
    """채팅 메시지 처리"""
    try:
        data = request.get_json()
        user_message = data.get('message')
        chat_history = data.get('chat_history', [])
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'message': '메시지가 필요합니다.'
            }), 400
        
        # AI 응답 생성 (DB 우선, 없으면 LLM)
        response = get_ai_response(user_message, chat_history)

        # 대화 기록 저장
        save_chat_interaction(
            user_message,
            response.get('response', '응답을 생성할 수 없습니다.'),  # 기본값 설정
            response.get('pattern_type'),
            response.get('route_code'),
            response.get('type'),
            None,  # response_time
            response  # 전체 응답 JSON 저장
        )
        
        return jsonify({
            'status': 'success',
            'data': response
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'서버 오류가 발생했습니다. (에러: {str(e)})'
        }), 500

@chat_bp.route('/api/chat/history', methods=['GET'])
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

@chat_bp.route('/api/chat/popular', methods=['GET'])
def popular_questions():
    """인기 질문 목록 조회"""
    questions = get_popular_questions()
    return jsonify(questions) 