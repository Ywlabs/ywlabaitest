from openai import OpenAI
import os
from database import get_db_connection
import time
from common.logger import setup_logger
from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
import numpy as np
import json

# 로거 설정
logger = setup_logger('chat_service')

# OpenAI API 키 설정
openai_client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    timeout=20.0  # 20초 타임아웃 설정
)

def get_gpt_response(question, find_similar_question_func):
    """질문에 대한 GPT 응답 생성"""
    start_time = time.time()
    logger.info(f"[시작] 질문 처리 시작: {question}")
    
    try:
        # 1. 유사 질문 찾기
        logger.info("[1단계] 유사 질문 검색 시작")
        search_start = time.time()
        best_match = find_similar_question_func(question)
        search_time = time.time() - search_start
        
        if best_match:
            logger.info(f"[1단계 완료] 유사 질문 찾음 (소요시간: {search_time:.2f}초)")
            logger.info(f"찾은 유사 질문: {best_match.get('pattern_text')}")
            logger.info(f"유사도 점수: {best_match.get('similarity_score', 'N/A')}")
        else:
            logger.warning(f"[1단계 완료] 유사 질문을 찾지 못함 (소요시간: {search_time:.2f}초)")
        
        if best_match:
            # 2. GPT 응답 생성
            logger.info("[2단계] GPT 응답 생성 시작")
            gpt_start = time.time()
            
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for 영우랩스 company. Use the provided context to answer questions."},
                    {"role": "user", "content": f"Context: {best_match}\nQuestion: {question}"}
                ],
                max_tokens=500,  # 응답 길이 제한
                temperature=0.7  # 응답 다양성 조절
            )
            
            gpt_time = time.time() - gpt_start
            logger.info(f"[2단계 완료] GPT 응답 생성 완료 (소요시간: {gpt_time:.2f}초)")
            
            # 3. 응답 저장
            logger.info("[3단계] 응답 저장 시작")
            save_start = time.time()
            
            result = {
                'response': response.choices[0].message.content,
                'type': best_match.get('response_type'),
                'target_url': best_match.get('target_url'),
                'button_text': best_match.get('button_text')
            }
            
            save_time = time.time() - save_start
            logger.info(f"[3단계 완료] 응답 저장 완료 (소요시간: {save_time:.2f}초)")
            
            # 전체 처리 시간 로깅
            total_time = time.time() - start_time
            logger.info(f"[완료] 전체 처리 완료 (총 소요시간: {total_time:.2f}초)")
            logger.info(f"- 유사 질문 검색: {search_time:.2f}초")
            logger.info(f"- GPT 응답 생성: {gpt_time:.2f}초")
            logger.info(f"- 응답 저장: {save_time:.2f}초")
            
            return result
            
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"[에러] 처리 중 오류 발생 (소요시간: {error_time:.2f}초)")
        logger.error(f"에러 내용: {str(e)}")
        
        if "timeout" in str(e).lower():
            logger.error("GPT API 타임아웃 발생")
            return {
                'response': '죄송합니다. 응답 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.',
                'type': 'text',
                'target_url': None,
                'button_text': None
            }
    
    # 기본 응답
    total_time = time.time() - start_time
    logger.warning(f"[완료] 기본 응답 반환 (총 소요시간: {total_time:.2f}초)")
    return {
        'response': '죄송합니다. 질문을 이해하지 못했습니다. 다른 방식으로 질문해 주시겠어요?',
        'type': 'text',
        'target_url': None,
        'button_text': None
    }

def save_chat_interaction(user_message, ai_response, intent_tag, route_code):
    """대화 기록을 chat_history에 저장"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO chat_history 
                (user_message, ai_response, intent_tag, route_code)
                VALUES (%s, %s, %s, %s)
            ''', (
                user_message,
                ai_response,
                intent_tag,
                route_code
            ))
            conn.commit()
    finally:
        conn.close()

def get_chat_history():
    """채팅 히스토리 조회"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    ch.id,
                    ch.user_message,
                    ch.ai_response,
                    ch.intent_tag,
                    ch.route_code,
                    r.route_name,
                    r.route_path,
                    r.route_type,
                    ch.created_at
                FROM chat_history ch
                LEFT JOIN routes r ON ch.route_code = r.route_code
                ORDER BY ch.created_at DESC 
                LIMIT 10
            ''')
            history = cursor.fetchall()
            return [
                {
                    'id': item['id'],
                    'user_message': item['user_message'],
                    'ai_response': item['ai_response'],
                    'intent_tag': item['intent_tag'],
                    'route_code': item['route_code'],
                    'route_name': item['route_name'],
                    'route_path': item['route_path'],
                    'route_type': item['route_type'],
                    'created_at': item['created_at'].isoformat() if item['created_at'] else None
                }
                for item in history
            ]
    finally:
        conn.close()

def get_popular_questions():
    """인기 질문 목록 조회"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT user_message, COUNT(*) as count
                FROM chat_history
                GROUP BY user_message
                ORDER BY count DESC
                LIMIT 5
            ''')
            popular = cursor.fetchall()
            return [item['user_message'] for item in popular]  # 질문만 반환
    finally:
        conn.close()

def get_db_response(user_message, similar_question):
    """DB 기반 답변 생성 및 직원 정보 처리"""
    response = None
    if similar_question and similar_question.get('similarity_score', 0) > 0.6:  # 임계값 0.7에서 0.6으로 조정
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT r.response, r.response_type, r.route_code,
                           rt.route_name, rt.route_path, rt.route_type,
                           r.template_variables
                    FROM responses r
                    LEFT JOIN routes rt ON r.route_code = rt.route_code
                    WHERE r.intent_tag = %s AND r.is_active = 1
                ''', (similar_question['intent_tag'],))
                response_data = cursor.fetchone()
                if response_data:
                    # 직원 정보 intent일 때 동적 템플릿 처리
                    if similar_question['intent_tag'] == 'employee_info' and response_data['response_type'] == 'dynamic':
                        name = extract_employee_name(user_message)
                        employee_response = None
                        employee_dict = None
                        if name:
                            conn2 = get_db_connection()
                            try:
                                with conn2.cursor() as cursor2:
                                    cursor2.execute('''
                                        SELECT name, position, dept_nm, email, phone FROM employees WHERE name = %s
                                    ''', (name,))
                                    employee_dict = cursor2.fetchone()
                            finally:
                                conn2.close()
                            if employee_dict:
                                employee_response = get_employee_info_and_fill_template(name, response_data['response'])
                                response = {
                                    'status': 'success',
                                    'data': {
                                        'response': employee_response,
                                        'response_type': 'dynamic',
                                        'route_code': None,
                                        'route_name': None,
                                        'route_path': None,
                                        'route_type': None
                                    }
                                }
                            else:
                                response = {
                                    'status': 'success',
                                    'data': {
                                        'response': f'죄송합니다. {name}님의 정보를 찾을 수 없습니다.',
                                        'response_type': 'text',
                                        'route_code': None,
                                        'route_name': None,
                                        'route_path': None,
                                        'route_type': None
                                    }
                                }
                        else:
                            response = {
                                'status': 'success',
                                'data': {
                                    'response': '직원 이름을 입력해주세요.',
                                    'response_type': 'text',
                                    'route_code': None,
                                    'route_name': None,
                                    'route_path': None,
                                    'route_type': None
                                }
                            }
                    else:
                        # 템플릿 변수가 있는 경우 처리
                        template_vars = response_data.get('template_variables', {})
                        if template_vars:
                            response_text = response_data['response']
                            for var_name, var_value in template_vars.items():
                                response_text = response_text.replace(f'{{{var_name}}}', str(var_value))
                            response_data = dict(response_data)
                            response_data['response'] = response_text
                        
                        response = {
                            'status': 'success',
                            'data': {
                                'response': response_data['response'],
                                'response_type': response_data['response_type'],
                                'route_code': response_data['route_code'],
                                'route_name': response_data['route_name'],
                                'route_path': response_data['route_path'],
                                'route_type': response_data['route_type']
                            }
                        }
                else:
                    response = {
                        'status': 'success',
                        'data': {
                            'response': '죄송합니다. 응답을 찾을 수 없습니다.',
                            'response_type': 'text',
                            'route_code': None,
                            'route_name': None,
                            'route_path': None,
                            'route_type': None
                        }
                    }
        finally:
            conn.close()
    else:
        response = {
            'status': 'success',
            'data': {
                'response': '죄송합니다. 이해하지 못했습니다.',
                'response_type': 'text',
                'route_code': None,
                'route_name': None,
                'route_path': None,
                'route_type': None
            }
        }
        similar_question = {'intent_tag': None}
    return response, similar_question

def get_ai_response(user_message, similar_question, find_similar_question_func):
    """DB 기반 답변 우선, 없으면 LLM 생성 답변을 반환"""
    db_response, similar_question = get_db_response(user_message, similar_question)
    if not db_response or db_response['data']['response'] in ['죄송합니다. 이해하지 못했습니다.', None]:
        gpt_result = get_gpt_response(user_message, find_similar_question_func)
        response = {
            'status': 'success',
            'data': {
                'response': gpt_result['response'],
                'response_type': 'gpt',
                'route_code': None,
                'route_name': None,
                'route_path': None,
                'route_type': None
            }
        }
    else:
        response = db_response
    return response, similar_question 