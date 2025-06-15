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
from core.profiles.prompt_utils import format_system_prompt

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
    route_type: Optional[str] = None,
    route_name: Optional[str] = None,
    route_path: Optional[str] = None,
    employee: Optional[Dict] = None,
    metadata: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    응답 생성 함수
    - response: 사용자에게 보여줄 응답 메시지
    - response_type: 응답 타입 (text, dynamic)
    - route_code: 라우팅 코드
    - route_type: 라우트타입
    - route_name: 라우트이름 (버튼명)
    - route_path: 라우트패스
    - employee: 직원 정보 (dynamic 타입일 때)
    - metadata: 추가 메타데이터
    - route_type: 라우팅 타입 (internal, external)
    """
    response_data = {
        'response': response,  # 사용자에게 보여줄 응답 메시지
        'response_type': response_type,
        'timestamp': datetime.now().isoformat()
    }
    
    # 라우팅 정보가 있는 경우 추가
    if route_code or route_type:
        response_data.update({
            'route_code': route_code,
            'route_type': route_type,
            'route_name': route_name,
            'route_path': route_path
        })
    
    # 메타데이터가 있는 경우 추가
    if metadata:
        response_data['metadata'] = metadata
        
    return response_data

# GPT 응답 생성 함수
def get_gpt_response(question: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    [GPT 응답 생성]
    - 입력: 
        - question: 사용자의 질문(문자열)
        - chat_history: 이전 대화 기록 (선택)
    - 동작: 
        - 정책/규정 등 policy_collection에서 유사 질문을 찾고
        - 검색된 내용만을 기반으로 답변 생성
    - 출력: dict (response, type, route_code 등)
    """
    start_time = time.time()
    logger.info(f"[USER] 질문 입력: {question}")
    logger.info(f"[시작] 질문 처리 시작")
    try:
        # 1-1. Chroma DB에서 유사 문단(정책 등) 검색
        from services.chroma_service import get_similar_context_from_chroma
        chroma_context = get_similar_context_from_chroma(question)
        
        if not chroma_context:
            logger.warning("[GPT] 검색된 정책 내용이 없습니다.")
            return create_response(
                response="죄송합니다. 해당 내용에 대한 정책 정보를 찾을 수 없습니다.",
                response_type="none"
            )
            
        # 2. GPT 응답 생성 (LangChain ChatOpenAI)
        logger.info(f"[2단계] GPT 응답 생성 시작 (LangChain) [USER] {question}")
        gpt_start = time.time()
        
        # 2-1. 시스템 프롬프트 설정 (프로필에서 로드)
        system_prompt = format_system_prompt("policy_assistant")
        
        # 2-2. 메시지 구성
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"질문: {question}\n\n참고할 정책 내용:\n{chroma_context}"}
        ]
        
        # 2-3. GPT 호출
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.3,  # 더 일관된 답변을 위해 temperature 낮춤
            max_tokens=1000
        )
        
        # 2-4. 응답 처리
        gpt_response = response.choices[0].message.content
        logger.info(f"[2단계 완료] GPT 응답 생성 완료 (소요시간: {time.time() - gpt_start:.2f}초)")
        
        # 3. 응답 저장
        logger.info("[3단계] 응답 저장 시작")
        save_start = time.time()
        
        response_data = {
            "response": gpt_response,
            "response_type": "gpt",
            "route_code": None,
            "target_url": None,
            "button_text": None
        }
        
        logger.info(f"[GPT 응답] 응답 데이터: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        logger.info(f"[3단계 완료] 응답 저장 완료 (소요시간: {time.time() - save_start:.2f}초)")
        
        return response_data
        
    except Exception as e:
        logger.error(f"[에러] 처리 중 오류 발생 (소요시간: {time.time() - start_time:.2f}초)")
        logger.error(f"에러 내용: {str(e)}")
        return create_response(
            response="죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다.",
            response_type="none"
        )

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
                    try:
                        handler_module = importlib.import_module(f"core.handlers.{response_handler}")
                    except ModuleNotFoundError:
                        logger.warning(f"[핸들러] 핸들러 모듈을 찾을 수 없음: {response_handler}")
                        return create_response(
                            response="죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다.",
                            response_type="none"
                        )
                    handler_func = getattr(handler_module, 'handle')
                    handler_response = handler_func(user_message, meta, similar_qa.get('response'))
                    logger.info(f"[핸들러] 핸들러 응답: {handler_response}")
                    return handler_response
                except Exception as e:
                    logger.error(f"[핸들러] 핸들러 실행 실패: {str(e)}")
                    return create_response(
                        response="죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다.",
                        response_type="none"
                    )
            
            # 기본 응답 반환
            logger.info(f"[USER] 기본 응답 반환")
            return create_response(
                response=similar_qa.get('response'),
                response_type=similar_qa.get('response_type', 'text'),
                route_code=similar_qa.get('route_code'),
                route_path=meta.get('route_path'),
                route_name=meta.get('route_name'),
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
                response_type="none"
            )
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"[에러] 처리 중 오류 발생 (소요시간: {error_time:.2f}초)")
        logger.error(f"에러 내용: {str(e)}")
        return create_response(
            response="죄송합니다. 처리 중 오류가 발생했습니다.",
            response_type="none"
        )

def get_ai_response(question: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    [AI 응답 생성]
    - 입력: 
        - question: 사용자의 질문(문자열)
        - chat_history: 이전 대화 기록 (선택) : 연속된 질문을 위해 사용
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
        
        if db_response and db_response.get('response_type') != 'none':
            logger.info(f"[1단계 완료] DB 기반 응답 성공 (소요시간: {db_time:.2f}초)")
            return db_response
        else:
            logger.warning(f"[1단계 완료] DB 기반 응답 실패 (소요시간: {db_time:.2f}초)")
            
        # 2. GPT 기반 응답 생성 / 응답 타입이 none 이면 다음 단계 진행
        logger.info(f"[2단계] GPT 기반 응답 생성 시작 [USER] {question}")
        gpt_start = time.time()
        gpt_response = get_gpt_response(question, chat_history)
        gpt_time = time.time() - gpt_start
        
        # GPT 응답 로깅
        logger.info(f"[GPT 응답] 응답 데이터: {json.dumps(gpt_response, ensure_ascii=False, indent=2)}")
        
        if gpt_response:
            logger.info(f"[2단계 완료] GPT 기반 응답 생성 완료 (소요시간: {gpt_time:.2f}초)")
            return create_response(
                response=gpt_response.get('response', '검색된 결과가 존재 하지 않습니다.'),
                response_type="gpt",
            )
        else:
            logger.warning(f"[2단계 완료] GPT 기반 응답 생성 실패 (소요시간: {gpt_time:.2f}초)")
            return create_response(
                response="죄송합니다. 응답을 생성할 수 없습니다.",
                response_type="none"
            )
            
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"[에러] 처리 중 오류 발생 (소요시간: {error_time:.2f}초)")
        return create_response(
            response="죄송합니다. 처리 중 오류가 발생했습니다.",
            response_type="none"
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
