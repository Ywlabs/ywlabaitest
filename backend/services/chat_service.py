from openai import OpenAI
import os
from database import get_db_connection
import time
from common.logger import setup_logger
import json
from services.chroma_service import search_similar_in_collection, search_rag_documents
from config import config
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Optional
import importlib
from datetime import datetime
import logging
from core.profiles.prompt_utils import get_prompt_template, format_system_prompt
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# 로거 설정
logger = logging.getLogger(__name__)

# OpenAI API 키 설정
openai_client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    timeout=20.0
    )

def create_response(
    response: str,
    response_type: str = "text",
    route_code: Optional[str] = None,
    route_type: Optional[str] = None,
    route_name: Optional[str] = None,
    route_path: Optional[str] = None,
    employee: Optional[Dict] = None,
    metadata: Optional[Dict] = None
) -> Dict[str, Any]:
    response_data = {
        'response': response,
        'response_type': response_type,
        'timestamp': datetime.now().isoformat()
    }
    if route_code or route_type:
        response_data.update({
            'route_code': route_code,
            'route_type': route_type,
            'route_name': route_name,
            'route_path': route_path
        })
    if metadata:
        response_data['metadata'] = metadata
    return response_data

def get_db_response(user_message: str) -> Optional[Dict[str, Any]]:
    """
    DB 기반 응답(챗봇 기능)을 먼저 확인합니다.
    - 메뉴 이동, 지정된 답변, 동적 핸들러 등을 처리합니다.
    - 처리할 내용이 없으면 None을 반환합니다.
    """
    logger.info(f"[DB 응답 시도] 사용자 질문: {user_message}")
    
    docs = search_similar_in_collection("chatbot_collection", user_message, top_k=1)
    
    if not docs:
        logger.info("[DB 응답] 유사한 QnA를 찾지 못했습니다.")
        return None

    top_doc = docs[0]
    meta = top_doc.metadata
    similarity_score = meta.get('similarity_score', 0.0)
    
    # config에서 chatbot_collection의 임계값 가져오기
    chatbot_config = next((item for item in config.DB_CHROMA_COLLECTIONS if item["collection"] == "chatbot_collection"), None)
    similarity_threshold = chatbot_config.get("similarity_threshold", 0.9) if chatbot_config else 0.9 # 설정이 없으면 0.9를 기본값으로 사용
    
    # 동적 핸들러가 있거나, 유사도가 설정된 임계값보다 높을 때만 DB 응답으로 처리
    response_handler = meta.get('response_handler')
    if response_handler or similarity_score > similarity_threshold:
        logger.info(f"[DB 응답] 일치 항목 발견. 유사도: {similarity_score}, 임계값: {similarity_threshold}, 핸들러: {response_handler}")
        
        if response_handler:
            try:
                logger.info(f"[핸들러] 동적 핸들러 실행: {response_handler}")
                handler_module = importlib.import_module(f"core.handlers.{response_handler}")
                handler_func = getattr(handler_module, 'handle')
                return handler_func(user_message, meta, meta.get('response'))
            except Exception as e:
                logger.error(f"[핸들러] 핸들러 실행 실패: {str(e)}")
                return create_response("죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다.", "error")
        
        # 핸들러가 없는 단순 응답
        return create_response(
            response=meta.get('response'),
            response_type=meta.get('response_type', 'text'),
            route_code=meta.get('route_code'),
            route_path=meta.get('route_path'),
            route_name=meta.get('route_name'),
            route_type=meta.get('route_type'),
            metadata={
                'pattern_id': meta.get('pattern_id'),
                'pattern_text': top_doc.page_content,
                'similarity_score': similarity_score
            }
        )
    
    logger.info(f"[DB 응답] 일치 항목을 찾았으나, GPT로 처리하기 위해 건너뜁니다. (유사도: {similarity_score}, 임계값: {similarity_threshold})")
    return None

def get_gpt_response(question: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    RAG + LLM을 사용하여 문서 기반의 답변을 생성합니다.
    """
    logger.info(f"[GPT 응답 시도] 사용자 질문: {question}")
    
    # 1. RAG 문서 검색
    rag_docs = search_rag_documents(question)
    if not rag_docs:
        logger.warning("[GPT 응답] 관련 문서를 찾지 못했습니다.")
        return create_response("죄송합니다. 질문과 관련된 정보를 찾을 수 없습니다.", "not_found")
        
    context = "\n\n".join(doc.page_content for doc in rag_docs)

    # 2. LangChain을 사용한 답변 생성
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3, max_tokens=1500)
    # RAG 검색 결과는 policy_assistant 프롬프트를 사용해 정확하게 답변하도록 합니다.
    prompt = get_prompt_template("policy_assistant")
    
    if not prompt:
        return create_response("죄송합니다. 응답 생성에 필요한 프롬프트를 찾을 수 없습니다.", "error")

    chain = prompt | llm | StrOutputParser()
    
    ai_message = chain.invoke({
        "context": context,
        "question": question
    })
    
    logger.info("[GPT 응답] 생성 완료")
    return create_response(response=ai_message, response_type="gpt")


def get_ai_response(question: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    AI 응답 생성의 메인 컨트롤러
    - 1순위: DB 기반의 직접 응답 (메뉴 이동 등)
    - 2순위: RAG + GPT 기반의 문서 검색 응답
    """
    start_time = time.time()
    logger.info(f"===== AI 응답 프로세스 시작: {question} =====")
    
    # 1. DB 기반 응답 시도 (챗봇 기능)
    db_response = get_db_response(question)
    if db_response:
        logger.info(f"[최종 응답] DB 기반 응답 반환. (소요시간: {time.time() - start_time:.2f}초)")
        return db_response
        
    # 2. RAG + GPT 기반 응답 시도
    gpt_response = get_gpt_response(question, chat_history)
    
    # gpt 응답 결과가 not_found일때 최종적으로 응답할 메세지
    if gpt_response.get('response_type') == 'not_found':
        return create_response("죄송합니다. 현재 질문에 대해 답변할 수 있는 정보가 없습니다. 다른 질문을 해주시거나 관리자에게 문의해주세요.", "text")

    logger.info(f"[최종 응답] GPT 기반 응답 반환. (소요시간: {time.time() - start_time:.2f}초)")
    return gpt_response

def save_chat_interaction(user_message, ai_response, intent_tag, route_code, response_source, response_time, response_json=None):
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
                    ch.response_source,
                    ch.created_at,
                    ch.response_json
                FROM chat_history ch
                LEFT JOIN routes r ON ch.route_code = r.route_code
                ORDER BY ch.created_at DESC 
            ''')
            rows = cursor.fetchall()
            history = []
            for row in rows:
                history.append({
                    'id': row['id'],
                    'user_message': row['user_message'],
                    'ai_response': row['ai_response'],
                    'intent_tag': row['intent_tag'],
                    'route_code': row['route_code'],
                    'route_name': row['route_name'],
                    'route_path': row['route_path'],
                    'route_type': row['route_type'],
                    'response_source': row['response_source'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    'response_json': row['response_json']
                })
            return history
    finally:
        conn.close()

def get_popular_questions():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT user_message, COUNT(*) as count
                FROM chat_history
                WHERE intent_tag = 'qna' OR intent_tag IS NULL
                GROUP BY user_message
                ORDER BY count DESC
                LIMIT 5
            ''')
            # 프론트엔드 호환성을 위해 질문 문자열 리스트를 반환합니다.
            return [row['user_message'] for row in cursor.fetchall()]
    finally:
        conn.close()
