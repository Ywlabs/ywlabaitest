from openai import OpenAI
import os
from database import get_db_connection
import time
from common.logger import setup_logger
from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
import numpy as np
import json
from services.chroma_service import search_similar_in_collection
from config import Config
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from core.embeddings.hf_embedding import get_hf_embedding
from core.handlers.intent_handler_map import INTENT_HANDLER_MAP

# 로거 설정
logger = setup_logger('chat_service')

# OpenAI API 키 설정
openai_client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    timeout=20.0  # 20초 타임아웃 설정
)


def get_gpt_response(question):
    """
    [GPT 응답 생성]
    - 입력: 사용자의 질문(문자열)
    - 동작: 정책/규정 등 policy_collection에서 유사 질문을 찾고, 없으면 RAG+GPT로 답변 생성
    - 출력: dict (response, type, route_code 등)
    """
    start_time = time.time()
    logger.info(f"[USER] 질문 입력: {question}")
    logger.info(f"[시작] 질문 처리 시작")
    try:
        # 1. 유사 질문 찾기 (ChromaDB 기반)
        logger.info(f"[1단계] 유사 질문 검색 시작 (ChromaDB) [USER] {question}")
        search_start = time.time()
        docs = search_similar_in_collection("policy_collection", question, top_k=1)
        similar_question = None
        if docs:
            doc = docs[0]
            meta = doc.metadata
            similar_question = {
                'pattern_id': meta.get('pattern_id'),
                'pattern_text': doc.page_content,
                'response': meta.get('response'),
                'pattern_type': meta.get('pattern_type'),
                'response_type': meta.get('response_type'),
                'route_code': meta.get('route_code'),
                'similarity_score': 1.0
            }
        search_time = time.time() - search_start
        if similar_question:
            logger.info(f"[1단계 완료] 유사 질문 찾음 (소요시간: {search_time:.2f}초) [USER] {question}")
            logger.info(f"[USER] 찾은 유사 질문: {similar_question.get('pattern_text')}")
            logger.info(f"유사도 점수: {similar_question.get('similarity_score', 'N/A')}")
            # intent_tag 추출 (pattern_type 또는 intent_tag)
            intent_tag = similar_question.get("intent_tag")
            response = similar_question.get("response")
            handler = INTENT_HANDLER_MAP.get(intent_tag)
            if handler:
                logger.info(f"[USER] 핸들러({intent_tag}) 호출")
                return handler(question, similar_question, response)[0]  # (응답, meta) 중 응답만 반환
            # 핸들러 없으면 기본 응답
            logger.info(f"[USER] 핸들러 없음, 기본 응답 반환")
            return {
                'response': response,
                'type': 'db',
                'route_code': similar_question.get('route_code'),
                'pattern_id': similar_question.get('pattern_id'),
                'pattern_text': similar_question.get('pattern_text'),
                'pattern_type': similar_question.get('pattern_type'),
                'response_type': similar_question.get('response_type'),
            }
        else:
            logger.warning(f"[1단계 완료] 유사 질문을 찾지 못함 또는 임계값 미달 (소요시간: {search_time:.2f}초) [USER] {question}")
        # 1-2. Chroma DB에서 유사 문단(정책 등) 검색 (RAG_CHROMA_COLLECTIONS 기반)
        from services.chroma_service import get_similar_context_from_chroma
        chroma_context = get_similar_context_from_chroma(question)
        # 2. GPT 응답 생성 (LangChain ChatOpenAI)
        logger.info(f"[2단계] GPT 응답 생성 시작 (LangChain) [USER] {question}")
        gpt_start = time.time()
        system_prompt = f"""
        당신은 영우랩스의 도우미 어시스턴트입니다. 답변은 반드시 마크다운(Markdown) 문법을 엄격히 지켜서 작성하세요.
        - 기존에 존재하는 정책 문서를 참고하여 내용변경은 하지 말고, 친절한 답변형태로 작성하세요.
        - GPT에서 생성한 추가답변은 별도 항목으로 분리하여 작성해주세요.
        - 여러 항목은 반드시 아래 예시처럼 줄바꿈과 함께 마크다운 리스트(- 또는 1. 2. 등)로 작성하세요.
        - 표가 필요하면 반드시 아래 예시처럼 각 행마다 줄바꿈을 넣어 마크다운 표로 작성하세요.
        - 표 셀에는 줄바꿈 없이 간결하게 작성하세요.
        - 리스트와 표를 혼합하지 말고, 표는 표만, 리스트는 리스트만 사용하세요.
        - 코드 예시가 필요하면 마크다운 코드블록(```)을 사용하세요.
        예시(반드시 줄바꿈 포함):
        - 복지 제도
        - 복지포인트
        - 사내 기부금 관리
        - 사내 사회공헌 활동
        | 항목 | 내용 |
        |------|------|
        | 복지포인트 | 연 1회 지급, 복지몰 사용 가능 |
        | 사내 기부금 관리 | 연 1회 공지, 지정 계좌 접수 |
        | 사내 사회공헌 활동 | 연 2회 이상 실시 |
{chroma_context}
"""
        user_prompt = f"질문: {question}\n답변은 반드시 마크다운(Markdown) 문법을 엄격히 지켜서, 줄바꿈을 반드시 사용해 표와 리스트를 구분해서 작성해 주세요. 예시처럼 각 행마다 줄바꿈을 넣어주세요."
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            max_tokens=500,
            request_timeout=20.0,
        )
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        response = llm(messages)
        gpt_time = time.time() - gpt_start
        logger.info(f"[2단계 완료] GPT 응답 생성 완료 (소요시간: {gpt_time:.2f}초)")
        # 3. 응답 저장
        logger.info("[3단계] 응답 저장 시작")
        save_start = time.time()
        result = {
            'response': response.content,
            'type': 'gpt',
            'route_code': None,
            'target_url': None,
            'button_text': None
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
                LIMIT 5
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

def get_db_response(user_message):
    """
    [DB QnA 응답 생성]
    - 입력: 사용자의 질문(문자열)
    - 동작: chatbot 컬렉션에서 유사 QnA 검색, intent별 핸들러 처리, 기본 응답/에러 응답 구분
    - 출력: (dict(응답), dict(meta))
    """
    logger.info(f"[USER] 질문 입력: {user_message}")
    # 1. ChromaDB에서 유사 QnA 검색
    docs = search_similar_in_collection("chatbot", user_message, top_k=1)
    if not docs:
        logger.info(f"[get_db_response] ChromaDB에서 유사 QnA 없음 [USER] {user_message}")
        return {
            'status': 'success',
            'data': {
                'response': '죄송합니다. 이해하지 못했습니다.',
                'response_type': 'not_found',  # 명확하게 지정
                'route_code': None,
                'route_name': None,
                'route_path': None,
                'route_type': None
            }
        }, None
    doc = docs[0]
    # 유사도 임계값 적용 (없으면 1.0)
    similarity_score = getattr(doc, 'similarity_score', 1.0)
    if similarity_score < 0.7:
        logger.info(f"[get_db_response] 유사도 임계값 미달: {similarity_score} [USER] {user_message}")
        return {
            'status': 'success',
            'data': {
                'response': '죄송합니다. 이해하지 못했습니다.',
                'response_type': 'not_found',
                'route_code': None,
                'route_name': None,
                'route_path': None,
                'route_type': None
            }
        }, None
    meta = doc.metadata
    intent_tag = meta.get("intent_tag") or meta.get("pattern_type")
    response = meta.get("response")
    route_code = meta.get("route_code")
    handler = INTENT_HANDLER_MAP.get(intent_tag)
    logger.info(f"[get_db_response] meta: {meta} [USER] {user_message}")
    if handler:
        logger.info(f"[USER] 핸들러({intent_tag}) 호출")
        base_response, handler_meta = handler(user_message, meta, response)
        logger.info(f"[get_db_response] handler 사용, base_response: {base_response}, handler_meta: {handler_meta} [USER] {user_message}")
    else:
        response_type = meta.get("response_type") if meta.get("response_type") else "default"  # 없으면 default로
        logger.info(f"[USER] 핸들러 없음, 기본 응답 반환")
        base_response = {
            'status': 'success',
            'data': {
                'response': response,
                'response_type': response_type,
                'route_code': route_code if route_code is not None else '',
                'route_name': meta.get('route_name') if meta.get('route_name') is not None else '',
                'route_path': meta.get('route_path') if meta.get('route_path') is not None else '',
                'route_type': meta.get('route_type') if meta.get('route_type') is not None else ''
            }
        }
        handler_meta = meta
        logger.info(f"[get_db_response] handler 없음, base_response: {base_response}, handler_meta: {handler_meta} [USER] {user_message}")
    return base_response, meta  # 항상 meta 반환

def get_ai_response(user_message, similar_question):
    """
    [최종 AI 응답 생성]
    - 입력: user_message(질문), similar_question(유사 QnA 메타)
    - 동작: DB QnA 우선, 없으면 GPT 생성 답변. 기본/에러 응답(response_type)일 경우 GPT로 넘김
    - 출력: (dict(응답), dict(meta))
    """
    logger.info(f"[USER] 질문 입력: {user_message}")
    db_response, similar_question = get_db_response(user_message)
    logger.info(f"[get_ai_response] db_response: {db_response}, similar_question: {similar_question} [USER] {user_message}")
    intent_tag = None
    pattern_type = None
    if similar_question:
        intent_tag = similar_question.get('intent_tag')
        pattern_type = similar_question.get('pattern_type')
    response_type = db_response['data'].get('response_type') if db_response and 'data' in db_response else None
    if (
        not db_response
        or response_type in ['default', 'error', 'not_found']
        or not similar_question
        or (intent_tag is None and pattern_type is None)
    ):
        logger.info(f"[get_ai_response] GPT로 넘김: db_response={db_response}, similar_question={similar_question} [USER] {user_message}")
        gpt_result = get_gpt_response(user_message)
        if gpt_result is None:
            response = {
                'status': 'success',
                'data': {
                    'response': 'AI 응답을 생성하지 못했습니다. 잠시 후 다시 시도해 주세요.',
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
                    'response': gpt_result['response'],
                    'response_type': 'gpt',
                    'route_code': None,
                    'route_name': None,
                    'route_path': None,
                    'route_type': None
                }
            }
    else:
        logger.info(f"[get_ai_response] DB 응답 사용: {db_response} [USER] {user_message}")
        response = db_response
    return response, similar_question 