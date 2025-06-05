from openai import OpenAI
import os
from database import get_db_connection
import time
from common.logger import setup_logger
from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
import numpy as np
import json
from services.vector_service import model

# 로거 설정
logger = setup_logger('chat_service')

# OpenAI API 키 설정
openai_client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    timeout=20.0  # 20초 타임아웃 설정
)

def get_gpt_response(question, find_similar_question_func):
    """질문에 대한 GPT 응답 생성 (최신 DB 구조 반영)"""
    start_time = time.time()
    logger.info(f"[시작] 질문 처리 시작: {question}")
    
    try:
        # 1. 유사 질문 찾기
        logger.info("[1단계] 유사 질문 검색 시작")
        search_start = time.time()
        message_vector = model.encode(question)
        similar_question = find_similar_question_func(message_vector)
        search_time = time.time() - search_start
        
        if similar_question:
            logger.info(f"[1단계 완료] 유사 질문 찾음 (소요시간: {search_time:.2f}초)")
            logger.info(f"찾은 유사 질문: {similar_question.get('pattern_text')}")
            logger.info(f"유사도 점수: {similar_question.get('similarity_score', 'N/A')}")
        else:
            logger.warning(f"[1단계 완료] 유사 질문을 찾지 못함 (소요시간: {search_time:.2f}초)")
        
        if similar_question:
            # 2. GPT 응답 생성
            logger.info("[2단계] GPT 응답 생성 시작")
            gpt_start = time.time()
            
            # 시스템 프롬프트 개선
            system_prompt = """당신은 영우랩스의 도우미 어시스턴트입니다. 다음과 같은 역할을 수행합니다:
            1. 주어진 컨텍스트를 바탕으로 정확하고 간결한 답변을 제공합니다
            2. 직원 정보에 대한 질문이면 관련된 상세 정보에 초점을 맞춥니다
            3. 회사 절차에 대한 질문이면 단계별 안내를 제공합니다
            4. 확실하지 않은 내용이 있다면, 그 한계를 인정하고 대안적인 정보 획득 방법을 제안합니다
            5. 항상 전문적이고 친근한 톤을 유지합니다
            6. 컨텍스트에 충분한 정보가 없다면, 그 사실을 말하고 추가 정보를 찾을 수 있는 방법을 제안합니다

            다음 사항을 기억하세요:
            - 답변은 구체적이고 명확해야 합니다
            - 여러 항목이 있는 경우 글머리 기호를 사용합니다
            - 관련 링크나 참조가 있다면 포함합니다
            - 회사 용어를 일관되게 사용합니다
            - 질문이 모호하다면 명확히 해달라고 요청합니다
            - 컨텍스트가 질문과 완전히 일치하지 않는다면, 어떤 정보가 있는지 설명합니다"""

            # 사용자 프롬프트 개선
            user_prompt = f"""컨텍스트: {similar_question.get('pattern_text')}
질문: {question}

컨텍스트를 바탕으로 도움이 되는 답변을 제공해주세요. 컨텍스트가 질문을 완전히 다루지 못한다면, 그 사실을 인정하고 가능한 최선의 답변을 제공해주세요. 확실하지 않은 부분이 있다면 그렇게 말씀해주세요."""

            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.6,  # 반복 방지
                frequency_penalty=0.3  # 다양성 증가
            )
            
            gpt_time = time.time() - gpt_start
            logger.info(f"[2단계 완료] GPT 응답 생성 완료 (소요시간: {gpt_time:.2f}초)")
            
            # 3. 응답 저장
            logger.info("[3단계] 응답 저장 시작")
            save_start = time.time()
            
            result = {
                'response': response.choices[0].message.content,
                'type': similar_question.get('response_type'),  # 'text' 또는 'dynamic' 등 텍스트 데이터 유형만 사용
                'route_code': similar_question.get('route_code'),  # 프론트엔드가 routes 테이블 참조해 UI 분기
                'target_url': similar_question.get('target_url'),
                'button_text': similar_question.get('button_text')
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
                'route_code': None,
                'target_url': None,
                'button_text': None
            }
    
    # 기본 응답
    total_time = time.time() - start_time
    logger.warning(f"[완료] 기본 응답 반환 (총 소요시간: {total_time:.2f}초)")
    return {
        'response': '죄송합니다. 질문을 이해하지 못했습니다. 다른 방식으로 질문해 주시겠어요?',
        'type': 'text',
        'route_code': None,
        'target_url': None,
        'button_text': None
    }

def save_chat_interaction(user_message, ai_response, intent_tag, route_code, response_source, response_time, response_json=None):
    """대화 기록을 chat_history에 저장 (전체 응답 JSON 포함)"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO chat_history 
                (user_message, ai_response, intent_tag, route_code, response_source, response_time, response_json)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                user_message,
                ai_response,
                intent_tag,
                route_code,
                response_source,
                response_time,
                json.dumps(response_json, ensure_ascii=False) if response_json else None
            ))
            conn.commit()
    finally:
        conn.close()

def get_chat_history():
    """채팅 히스토리 조회 (전체 응답 JSON 포함)"""
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
                    ch.created_at,
                    ch.response_json
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
                    'created_at': item['created_at'].isoformat() if item['created_at'] else None,
                    'response_json': json.loads(item['response_json']) if item['response_json'] else None
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
    """DB 기반 답변 생성 및 직원 정보 처리 (상세 디버깅 로그 추가)"""
    logger.info(f"[get_db_response] 입력 user_message: {user_message}")
    logger.info(f"[get_db_response] 입력 similar_question: {similar_question}")
    response = None
    if similar_question and similar_question.get('similarity_score', 0) > 0.7:  # 임계값 0.7
        logger.info(f"[get_db_response] 유사도 임계값 통과: {similar_question.get('similarity_score')}")
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                logger.debug(f"[get_db_response] DB에서 intent_tag={similar_question['intent_tag']}로 응답 조회")
                cursor.execute('''
                    SELECT r.response, r.response_type, r.route_code,
                           rt.route_name, rt.route_path, rt.route_type,
                           r.template_variables
                    FROM responses r
                    LEFT JOIN routes rt ON r.route_code = rt.route_code
                    WHERE r.intent_tag = %s AND r.is_active = 1
                ''', (similar_question['intent_tag'],))
                response_data = cursor.fetchone()
                logger.debug(f"[get_db_response] DB 응답 데이터: {response_data}")
                if response_data:
                    # 직원 정보 intent일 때 동적 템플릿 처리
                    if similar_question['intent_tag'] == 'employee_info' and response_data['response_type'] == 'dynamic':
                        name = extract_employee_name(user_message)
                        logger.info(f"[get_db_response] 추출된 직원 이름: {name}")
                        employee_response = None
                        employee_dict = None
                        if name:
                            conn2 = get_db_connection()
                            try:
                                with conn2.cursor() as cursor2:
                                    logger.debug(f"[get_db_response] 직원 DB에서 name={name}으로 정보 조회")
                                    cursor2.execute('''
                                        SELECT name, position, dept_nm, email, phone FROM employees WHERE name = %s
                                    ''', (name,))
                                    employee_dict = cursor2.fetchone()
                                    logger.debug(f"[get_db_response] 직원 정보: {employee_dict}")
                            finally:
                                conn2.close()
                            if employee_dict:
                                employee_response = get_employee_info_and_fill_template(name, response_data['response'])
                                logger.info(f"[get_db_response] 직원 템플릿 응답: {employee_response}")
                                response = {
                                    'status': 'success',
                                    'data': {
                                        'response': employee_response,
                                        'response_type': 'dynamic',
                                        'employee': employee_dict,  # 직원 정보 객체 포함
                                        'route_code': None,
                                        'route_name': None,
                                        'route_path': None,
                                        'route_type': None
                                    }
                                }
                            else:
                                logger.warning(f"[get_db_response] 직원 정보 없음: {name}")
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
                            logger.warning(f"[get_db_response] 직원 이름 추출 실패")
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
                        # 템플릿 변수 항상 먼저 가져오기 및 로깅
                        template_vars = response_data.get('template_variables')
                        logger.info(f"DB에서 읽은 template_variables: {template_vars}")
                        if not template_vars:
                            template_vars = {}
                        if isinstance(template_vars, str):
                            try:
                                template_vars = json.loads(template_vars)
                            except Exception:
                                template_vars = {}
                        # sales_status(매출) intent일 때 user_message에서 연도 추출
                        if similar_question['intent_tag'] == 'sales_status':
                            import re
                            match = re.search(r'(20[0-9]{2})년', user_message)
                            if match:
                                year = int(match.group(1))
                                template_vars['year'] = year
                        logger.debug(f"[get_db_response] 템플릿 변수: {template_vars}")
                        if template_vars:
                            response_text = response_data['response']
                            for var_name, var_value in template_vars.items():
                                # 1중 중괄호로 치환
                                response_text = response_text.replace(f'{{{var_name}}}', str(var_value))
                            logger.info(f"[get_db_response] 치환된 response_text: {response_text}")
                            response_data = dict(response_data)
                            response_data['response'] = response_text
                        logger.info(f"DB에서 읽은 template_variables: {response_data['template_variables']}")
                        response = {
                            'status': 'success',
                            'data': {
                                'response': response_data['response'],
                                'response_type': response_data['response_type'],
                                'route_code': response_data['route_code'],
                                'route_name': response_data['route_name'],
                                'route_path': response_data['route_path'],
                                'route_type': response_data['route_type'],
                                'response_params': template_vars  # 위젯용 파라미터(연도 등) 추가
                            }
                        }
                else:
                    logger.warning(f"[get_db_response] DB에서 intent에 해당하는 응답 없음")
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
        logger.info(f"[get_db_response] 유사도 임계값 미달 또는 유사 질문 없음")
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
    logger.info(f"[get_db_response] 최종 반환 response: {response}")
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