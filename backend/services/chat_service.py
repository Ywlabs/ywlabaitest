from openai import OpenAI
import os
from database import get_db_connection
import time
from common.logger import setup_logger
from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
import numpy as np
import json
from services.chroma_service import search_similar_in_collection
from config import config
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage, FunctionMessage, ChatMessage
from core.embeddings.hf_embedding import get_hf_embedding
from typing import Dict, Any, List, Optional
import importlib
from datetime import datetime
import logging
import re
from core.utils.date_utils import extract_year
from core.utils.employee_utils import extract_employee_name

# 로거 설정
logger = logging.getLogger(__name__)

# OpenAI API 키 설정
openai_client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    timeout=20.0  # 20초 타임아웃 설정
)

def create_function_message(function_name: str, content: str) -> FunctionMessage:
    """
    FunctionMessage 생성
    - 입력: function_name(함수명), content(함수 실행 결과)
    - 출력: FunctionMessage 객체
    """
    return FunctionMessage(
        content=content,
        name=function_name
    )

def create_response(
    response: str,
    response_type: str = "text",
    route_code: Optional[str] = None,
    target_url: Optional[str] = None,
    button_text: Optional[str] = None,
    employee: Optional[Dict] = None,
    metadata: Optional[Dict] = None,
    route_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    응답 생성 함수
    - response: 사용자에게 보여줄 응답 메시지
    - response_type: 응답 타입 (text, dynamic)
    - route_code: 라우팅 코드
    - target_url: 이동할 URL
    - button_text: 버튼 텍스트
    - employee: 직원 정보 (dynamic 타입일 때)
    - metadata: 추가 메타데이터
    - route_type: 라우팅 타입 (internal, external)
    """
    response_data = {
        'response': response,  # 사용자에게 보여줄 응답 메시지
        'type': response_type,
        'timestamp': datetime.now().isoformat()
    }
    
    # 라우팅 정보가 있는 경우 추가
    if route_code or target_url:
        response_data.update({
            'route_code': route_code,
            'route_type': route_type,
            'route_name': button_text,
            'route_path': target_url
        })
    
    # 직원 정보가 있는 경우 추가
    if employee:
        response_data['employee'] = employee
        
    # 메타데이터가 있는 경우 추가
    if metadata:
        response_data['metadata'] = metadata
        
    return response_data

def get_gpt_response(question: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    [GPT 응답 생성]
    - 입력: 
        - question: 사용자의 질문(문자열)
        - chat_history: 이전 대화 기록 (선택)
    - 동작: 
        - 정책/규정 등 policy_collection에서 유사 질문을 찾고
        - 없으면 RAG+GPT로 답변 생성
        - user_prompt 내용 기반으로 function_message 생성
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
                'domain': meta.get('domain'),
                'category': meta.get('category'),
                'similarity_score': meta.get('similarity_score', 0.0)
            }
        search_time = time.time() - search_start
        if similar_question:
            logger.info(f"[1단계 완료] 유사 질문 찾음 (소요시간: {search_time:.2f}초) [USER] {question}")
            logger.info(f"[USER] 찾은 유사 질문: {similar_question.get('pattern_text')}")
            logger.info(f"유사도 점수: {similar_question.get('similarity_score', 'N/A')}")
            
            # response_handler가 있는 경우 동적 핸들러 실행
            response_handler = meta.get('response_handler')
            if response_handler:
                try:
                    logger.info(f"[핸들러] 동적 핸들러 실행: {response_handler}")
                    handler_module = importlib.import_module(f"core.handlers.{response_handler}")
                    handler_func = getattr(handler_module, 'handle')
                    handler_response = handler_func(question, meta, similar_question.get('response'))
                    logger.info(f"[핸들러] 핸들러 응답: {handler_response}")
                    return handler_response
                except Exception as e:
                    logger.error(f"[핸들러] 핸들러 실행 실패: {str(e)}")
                    return create_response(
                        response="죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다.",
                        response_type="text"
                    )
            
            # 기본 응답 반환
            logger.info(f"[USER] 기본 응답 반환")
            return create_response(
                response=similar_question.get('response'),
                response_type=similar_question.get('response_type', 'text'),
                route_code=similar_question.get('route_code'),
                target_url=meta.get('route_path'),
                button_text=meta.get('route_name'),
                route_type=meta.get('route_type'),
                metadata={
                    'domain': similar_question.get('domain'),
                    'category': similar_question.get('category'),
                    'pattern_id': similar_question.get('pattern_id'),
                    'pattern_text': similar_question.get('pattern_text'),
                    'pattern_type': similar_question.get('pattern_type')
                }
            )
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
            temperature=0.5,  # 더 일관된 답변을 위해 낮춤
            max_tokens=800,  # 더 자세한 설명을 위해 증가
            request_timeout=20.0,  # 현재 값 유지
        )
        
        # 메시지 리스트 구성
        messages = [SystemMessage(content=system_prompt)]
        
        # function_mapping.json의 매핑을 사용하여 function_message 생성
        function_messages = []
        for intent, mapping in config.function_mappings.items():
            if any(keyword in question.lower() for keyword in mapping['keywords']):
                # 핸들러 모듈 동적 임포트
                handler_module = importlib.import_module(mapping['handler'])
                handler_func = getattr(handler_module, mapping['function_name'])
                
                # 핸들러 호출 결과를 FunctionMessage로 전달
                function_messages.append(create_function_message(
                    function_name=mapping['function_name'],
                    content=handler_func(question, None, None)[0]
                ))
                logger.info(f"[Function Message] {mapping['function_name']} 함수 메시지 추가")
        
        # function_message가 있는 경우에만 추가
        if function_messages:
            messages.extend(function_messages)
            logger.info(f"[Function Message] 총 {len(function_messages)}개의 함수 메시지 추가")
        
        # 현재 질문 추가
        messages.append(HumanMessage(content=user_prompt))
        
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
        return result
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"[에러] 처리 중 오류 발생 (소요시간: {error_time:.2f}초)")
        logger.error(f"에러 내용: {str(e)}")
        return {
            'response': '죄송합니다. 처리 중 오류가 발생했습니다.',
            'type': 'error',
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

def get_db_response(user_message: str) -> Dict[str, Any]:
    """
    [DB 응답 생성]
    - 입력: user_message (사용자 메시지)
    - 동작: 
        - chatbot_collection에서 유사 QnA 검색 (무조건 chatbot_collection 사용)
        - 유사도 점수와 도메인/카테고리 기반 필터링
        - response_handler가 있는 경우 동적 핸들러 실행
    - 출력: dict (response, type, route_code 등)
    """
    start_time = time.time()
    logger.info(f"[USER] 질문 입력: {user_message}")
    logger.info(f"[시작] DB 응답 생성 시작")
    
    try:
        # 1. 유사 QnA 검색
        logger.info(f"[1단계] 유사 QnA 검색 시작 (ChromaDB) [USER] {user_message}")
        search_start = time.time()
        
        # 컬렉션 설정에서 search_top_k 가져오기
        collection_config = next((item for item in config.DB_CHROMA_COLLECTIONS if item["collection"] == "chatbot_collection"), None)
        search_top_k = collection_config.get("search_top_k", 5) if collection_config else 5
        
        docs = search_similar_in_collection("chatbot_collection", user_message, top_k=search_top_k)
        search_time = time.time() - search_start  # search_time 정의 위치 이동
        
        similar_qa = None
        if docs:
            # 첫 번째 결과 사용 (이미 임계값 체크가 완료된 결과)
            doc = docs[0]
            meta = doc.metadata
            
            # 최종 선택된 결과 상세 로깅
            logger.info(f"[CHROMA] 최종 선택된 결과:")
            logger.info(f"[CHROMA] - 내용: {doc.page_content}")
            logger.info(f"[CHROMA] - 메타데이터: {json.dumps(meta, ensure_ascii=False, indent=2)}")
            
            similar_qa = {
                'pattern_id': meta.get('pattern_id'),
                'pattern_text': doc.page_content,
                'response': meta.get('response'),
                'pattern_type': meta.get('pattern_type'),
                'response_type': meta.get('response_type'),
                'route_code': meta.get('route_code'),
                'domain': meta.get('domain'),
                'category': meta.get('category'),
                'similarity_score': meta.get('similarity_score', 0.0)
            }
            logger.info(f"[1단계 완료] 유사 QnA 찾음 (소요시간: {search_time:.2f}초) [USER] {user_message}")
            logger.info(f"[USER] 찾은 유사 QnA: {similar_qa.get('pattern_text')}")
            logger.info(f"유사도 점수: {similar_qa.get('similarity_score', 'N/A')}")
            
            # response_handler가 있는 경우 동적 핸들러 실행
            response_handler = meta.get('response_handler')
            if response_handler:
                try:
                    logger.info(f"[핸들러] 동적 핸들러 실행: {response_handler}")
                    handler_module = importlib.import_module(f"core.handlers.{response_handler}")
                    handler_func = getattr(handler_module, 'handle')
                    handler_response = handler_func(user_message, meta, similar_qa.get('response'))
                    logger.info(f"[핸들러] 핸들러 응답: {handler_response}")
                    return handler_response
                except Exception as e:
                    logger.error(f"[핸들러] 핸들러 실행 실패: {str(e)}")
                    return create_response(
                        response="죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다.",
                        response_type="text"
                    )
            
            # 기본 응답 반환
            logger.info(f"[USER] 기본 응답 반환")
            return create_response(
                response=similar_qa.get('response'),
                response_type=similar_qa.get('response_type', 'text'),
                route_code=similar_qa.get('route_code'),
                target_url=meta.get('route_path'),
                button_text=meta.get('route_name'),
                route_type=meta.get('route_type'),
                metadata={
                    'pattern_id': similar_qa.get('pattern_id'),
                    'pattern_text': similar_qa.get('pattern_text'),
                    'pattern_type': similar_qa.get('pattern_type'),
                    'domain': similar_qa.get('domain'),
                    'category': similar_qa.get('category')
                }
            )
        else:
            logger.warning(f"[1단계 완료] 유사 QnA를 찾지 못함 (소요시간: {search_time:.2f}초) [USER] {user_message}")
            return create_response(
                response="죄송합니다. 관련된 답변을 찾을 수 없습니다.",
                response_type="text"
            )
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"[에러] 처리 중 오류 발생 (소요시간: {error_time:.2f}초)")
        logger.error(f"에러 내용: {str(e)}")
        return create_response(
            response="죄송합니다. 처리 중 오류가 발생했습니다.",
            response_type="text"
        )

def get_ai_response(question: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    [AI 응답 생성]
    - 입력: 
        - question: 사용자의 질문(문자열)
        - chat_history: 이전 대화 기록 (선택)
    - 동작: 
        - DB 기반 응답 시도
        - 실패 시 GPT 기반 응답 생성
    - 출력: dict (response, type, route_code 등)
    """
    start_time = time.time()
    logger.info(f"[USER] 질문 입력: {question}")
    logger.info(f"[시작] 질문 처리 시작")
    try:
        # 1. DB 기반 응답 시도
        logger.info(f"[1단계] DB 기반 응답 시도 [USER] {question}")
        db_start = time.time()
        db_response = get_db_response(question)
        db_time = time.time() - db_start
        
        # DB 응답 로깅
        logger.info(f"[DB 응답] 응답 데이터: {json.dumps(db_response, ensure_ascii=False, indent=2)}")
        
        if db_response and db_response.get('response_type') != 'text':
            logger.info(f"[1단계 완료] DB 기반 응답 성공 (소요시간: {db_time:.2f}초)")
            return db_response
        else:
            logger.warning(f"[1단계 완료] DB 기반 응답 실패 (소요시간: {db_time:.2f}초)")
            
        # 2. GPT 기반 응답 생성
        logger.info(f"[2단계] GPT 기반 응답 생성 시작 [USER] {question}")
        gpt_start = time.time()
        gpt_response = get_gpt_response(question, chat_history)
        gpt_time = time.time() - gpt_start
        
        # GPT 응답 로깅
        logger.info(f"[GPT 응답] 응답 데이터: {json.dumps(gpt_response, ensure_ascii=False, indent=2)}")
        
        if gpt_response:
            logger.info(f"[2단계 완료] GPT 기반 응답 생성 완료 (소요시간: {gpt_time:.2f}초)")
            return create_response(
                response=gpt_response.get('response', '응답을 생성할 수 없습니다.'),
                response_type="gpt",
                route_code=gpt_response.get('route_code'),
                target_url=gpt_response.get('target_url'),
                button_text=gpt_response.get('button_text'),
                route_type=gpt_response.get('route_type')
            )
        else:
            logger.warning(f"[2단계 완료] GPT 기반 응답 생성 실패 (소요시간: {gpt_time:.2f}초)")
            return create_response(
                response="죄송합니다. 응답을 생성할 수 없습니다.",
                response_type="text"
            )
            
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"[에러] 처리 중 오류 발생 (소요시간: {error_time:.2f}초)")
        return create_response(
            response="죄송합니다. 처리 중 오류가 발생했습니다.",
            response_type="text"
        )

def initialize_db_collections():
    """DB 컬렉션 초기화"""
    try:
        # 컬렉션 설정 로드
        collections = config.DB_CHROMA_COLLECTIONS
        
        # 각 컬렉션 초기화
        for item in collections:
            collection_name = item["collection"]
            logger.info(f"[CHROMA] 컬렉션 초기화 시작: {collection_name}")
            try:
                # 1. 기존 컬렉션 삭제
                if collection_name in openai_client.list_collections():
                    openai_client.delete_collection(collection_name)
                    logger.info(f"[CHROMA] 기존 컬렉션 삭제됨: {collection_name}")
                # 2. 새 컬렉션 생성
                metadata = {
                    "hnsw:space": "cosine",
                    "hnsw:construction_ef": 100,
                    "hnsw:search_ef": 100,
                    "hnsw:M": 16,
                    "embedding_model": item["embedding_model"],
                    "type": item["type"],
                    "parser": item["parser"],
                    "search_top_k": item["search_top_k"],
                    "similarity_threshold": item.get("similarity_threshold", 0.7)  # 임계값 추가
                }
                collection = openai_client.create_collection(
                    name=collection_name,
                    metadata=metadata
                )
                logger.info(f"[CHROMA] 새 컬렉션 생성됨: {collection_name} (metadata: {metadata})")
                # 3. 데이터 로드 함수 가져오기
                get_all_func = get_func_from_str(item["get_all_func"])
                to_doc_func = get_func_from_str(item["to_doc_func"])
                # 4. 데이터 로드 및 변환
                raw_docs = get_all_func()
                documents = [to_doc_func(doc) for doc in raw_docs]
                # 5. 데이터가 있으면 컬렉션 업데이트
                if documents:
                    filtered_metadatas = []
                    for doc in documents:
                        metadata = {k: v for k, v in doc.metadata.items() if v is not None}
                        filtered_metadatas.append(metadata)
                        if collection_name == "chatbot_collection":
                            logger.info(f"[CHROMA] 추가 문서: pattern_id={metadata.get('pattern_id')}, "
                                        f"pattern={doc.page_content[:100]}..., "
                                        f"domain={metadata.get('domain')}, "
                                        f"category={metadata.get('category')}, "
                                        f"threshold={metadata.get('similarity_threshold')}")
                    try:
                        embeddings = get_hf_embedding(item["embedding_model"])
                        texts = [doc.page_content for doc in documents]
                        embeddings_list = embeddings.embed_documents(texts)
                        collection.add(
                            documents=texts,
                            embeddings=embeddings_list,
                            metadatas=filtered_metadatas,
                            ids=[str(i) for i in range(len(documents))]
                        )
                        logger.info(f"[CHROMA] {len(documents)}개 문서 추가됨: {collection_name}")
                    except Exception as e:
                        logger.error(f"[CHROMA] 임베딩 생성/저장 중 오류 발생: {str(e)}")
                        raise
                else:
                    logger.warning(f"[CHROMA] 추가할 문서 없음: {collection_name}")
            except Exception as e:
                logger.error(f"[CHROMA] 컬렉션 {collection_name} 처리 중 오류 발생: {str(e)}")
                continue
        logger.info("[CHROMA] 모든 컬렉션 초기화 완료")
    except Exception as e:
        logger.error(f"[CHROMA] 컬렉션 초기화 중 오류 발생: {str(e)}")
        raise
