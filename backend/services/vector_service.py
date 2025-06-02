import json
import numpy as np
from sentence_transformers import SentenceTransformer
from database import get_db_connection
from collections import OrderedDict
import time
from common.logger import setup_logger
from concurrent.futures import ThreadPoolExecutor
import threading
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache
import hashlib
import re

# 로거 설정
logger = setup_logger('vector_service')

# Sentence Transformer 모델 초기화
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# 캐시 크기 설정 (최근 1000개 쿼리 결과 캐싱)
CACHE_SIZE = 1000

class VectorStore:
    def __init__(self):
        self.metadata = {}  # pattern_id -> (pattern_text, response, target_url, button_text)
        self.vector_status = {}  # pattern_id -> status
        self._cache = {}  # 캐시 저장소
        self._cache_lock = threading.Lock()  # 캐시 동기화를 위한 락
        
    def _get_cache_key(self, question_vector):
        """캐시 키 생성"""
        # 벡터를 문자열로 변환하여 해시 생성
        vector_str = json.dumps(question_vector, sort_keys=True)
        return hashlib.md5(vector_str.encode()).hexdigest()
        
    def _get_from_cache(self, cache_key):
        """캐시에서 결과 조회"""
        with self._cache_lock:
            return self._cache.get(cache_key)
            
    def _save_to_cache(self, cache_key, result):
        """결과를 캐시에 저장"""
        with self._cache_lock:
            # 캐시 크기 제한
            if len(self._cache) >= CACHE_SIZE:
                # 가장 오래된 항목 제거
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            self._cache[cache_key] = result

    def _normalize_text(self, text):
        """텍스트 정규화"""
        # 소문자 변환 및 특수문자 제거
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()

    def _is_partial_match(self, pattern, text):
        """부분 문자열 매칭 검사"""
        pattern = self._normalize_text(pattern)
        text = self._normalize_text(text)
        return pattern in text

    def load_metadata(self):
        """메타데이터 로드"""
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # patterns와 responses 조인하여 메타데이터 가져오기
                cursor.execute('''
                    SELECT p.id as pattern_id, p.pattern as pattern_text, 
                           r.response, r.route_code,
                           p.pattern_type, p.is_active,
                           r.response_type, r.is_active as response_active
                    FROM patterns p
                    JOIN responses r ON p.intent_tag = r.intent_tag
                    LEFT JOIN vector_store vs ON p.id = vs.pattern_id
                    WHERE p.is_active = 1 AND r.is_active = 1
                ''')
                data = cursor.fetchall()
                
                # 메타데이터 저장
                self.metadata.clear()
                self.vector_status.clear()
                
                for item in data:
                    pattern_id = item['pattern_id']
                    self.metadata[pattern_id] = {
                        'pattern_text': item['pattern_text'],
                        'response': item['response'],
                        'route_code': item.get('route_code'),
                        'pattern_type': item['pattern_type'],
                        'response_type': item['response_type']
                    }
                    self.vector_status[pattern_id] = item.get('vector_status', 'pending')
                
                logger.info(f"메타데이터 로드 완료: {len(self.metadata)}개 패턴")
                return len(self.metadata)
        finally:
            conn.close()

    def update_vector(self, pattern_id, pattern_text):
        """단일 패턴의 벡터 업데이트"""
        try:
            # 벡터 생성
            vector = model.encode(pattern_text).tolist()
            
            # DB 업데이트
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO vector_store 
                    (pattern_id, vector, pattern_text, response, vector_status)
                    VALUES (%s, %s, %s, %s, 'completed')
                    ON DUPLICATE KEY UPDATE
                    vector = VALUES(vector),
                    vector_status = 'completed'
                ''', (
                    pattern_id,
                    json.dumps(vector),
                    pattern_text,
                    self.metadata[pattern_id]['response']
                ))
                conn.commit()
            
            self.vector_status[pattern_id] = 'completed'
            return True
        except Exception as e:
            logger.error(f"벡터 업데이트 실패 (pattern_id: {pattern_id}): {str(e)}")
            self.vector_status[pattern_id] = 'failed'
            return False

def find_similar_question(question_vector, top_k=1):
    """질문 벡터와 가장 유사한 벡터 찾기 (DB 기반)"""
    start_time = time.time()
    
    # NumPy 배열을 Python 리스트로 변환
    if isinstance(question_vector, np.ndarray):
        question_vector = question_vector.tolist()
    
    # 캐시 키 생성
    cache_key = vector_store._get_cache_key(question_vector)
    
    # 캐시에서 결과 확인
    cached_result = vector_store._get_from_cache(cache_key)
    if cached_result:
        logger.info("캐시된 결과 사용")
        return cached_result
    
    # DB에서 벡터 데이터 조회
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 먼저 patterns 테이블에서 키워드 매핑 정보를 가져옴
            cursor.execute('''
                SELECT DISTINCT intent_tag, pattern, priority
                FROM patterns
                WHERE is_active = 1
                ORDER BY priority DESC
            ''')
            intent_patterns = {}
            for row in cursor.fetchall():
                if row['intent_tag'] not in intent_patterns:
                    intent_patterns[row['intent_tag']] = []
                intent_patterns[row['intent_tag']].append({
                    'pattern': row['pattern'],
                    'priority': row['priority']
                })
            
            # 2. 키워드 기반 필터링 조건 생성
            keyword_filter = ""
            matched_intents = set()
            for intent_tag, patterns in intent_patterns.items():
                for pattern_info in patterns:
                    pattern = pattern_info['pattern']
                    if vector_store._is_partial_match(pattern, question_vector):
                        matched_intents.add(intent_tag)
                        break
            
            if matched_intents:
                keyword_filter = "OR p.intent_tag IN (" + ",".join([f"'{intent}'" for intent in matched_intents]) + ")"
            
            # 3. 벡터 데이터 조회
            cursor.execute(f'''
                SELECT 
                    vs.pattern_id,
                    vs.pattern_text,
                    vs.response,
                    p.pattern_type,
                    r.response_type,
                    r.route_code,
                    vs.vector,
                    p.intent_tag,
                    p.priority
                FROM vector_store vs
                JOIN patterns p ON vs.pattern_id = p.id
                JOIN responses r ON p.intent_tag = r.intent_tag
                WHERE vs.vector_status = 'completed'
                AND p.is_active = 1
                AND r.is_active = 1
                {keyword_filter}
            ''')
            results = cursor.fetchall()
            
            if not results:
                logger.warning("유사한 질문을 찾을 수 없음")
                return None
            
            # Python에서 유사도 계산
            max_similarity = -1
            best_match = None
            
            for result in results:
                stored_vector = np.array(json.loads(result['vector']), dtype=float)
                q_vector = np.array(question_vector, dtype=float)
                
                # 코사인 유사도 계산
                similarity = np.dot(q_vector, stored_vector) / (
                    np.linalg.norm(q_vector) * np.linalg.norm(stored_vector)
                )
                
                # 우선순위가 높은 패턴의 경우 유사도 보정
                if result['priority'] > 0:
                    similarity = similarity * (1 + (result['priority'] / 100))
                
                # 패턴 매칭 보너스
                intent_tag = result['intent_tag']
                if intent_tag in intent_patterns:
                    for pattern_info in intent_patterns[intent_tag]:
                        pattern = pattern_info['pattern']
                        if vector_store._is_partial_match(pattern, question_vector):
                            # 패턴의 우선순위에 따라 보너스 점수 조정
                            bonus = 1.2 + (pattern_info['priority'] / 100)
                            similarity = similarity * bonus
                            break
                
                # 최소 유사도 임계값 적용
                if similarity > 0.6:  # 임계값 조정
                    if similarity > max_similarity:
                        max_similarity = similarity
                        best_match = {
                            'pattern_id': result['pattern_id'],
                            'pattern_text': result['pattern_text'],
                            'response': result['response'],
                            'pattern_type': result['pattern_type'],
                            'response_type': result['response_type'],
                            'route_code': result['route_code'],
                            'intent_tag': result['intent_tag'],
                            'similarity_score': float(similarity)
                        }
            
            # 결과를 캐시에 저장
            if best_match:
                vector_store._save_to_cache(cache_key, best_match)
            
            logger.info(f"유사도 계산 완료 (소요시간: {time.time() - start_time:.2f}초)")
            return best_match
            
    except Exception as e:
        logger.error(f"유사 질문 검색 중 오류 발생: {str(e)}")
        return None
    finally:
        conn.close()

# 전역 VectorStore 인스턴스
vector_store = VectorStore()

def initialize_vector_store():
    """벡터 스토어 초기화"""
    logger.info("벡터 스토어 초기화 시작")
    
    try:
        # 1. 메타데이터 로드
        total_patterns = vector_store.load_metadata()
        logger.info(f"총 {total_patterns}개의 패턴 메타데이터 로드 완료")
        
        # 2. 벡터 상태 확인 및 생성
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 갱신이 필요한 패턴만 조회 (completed가 아닌 것들)
                cursor.execute('''
                    SELECT DISTINCT 
                        p.id, 
                        p.pattern, 
                        p.intent_tag,
                        r.response,
                        p.pattern_type,
                        r.response_type,
                        r.route_code,
                        vs.vector_status
                    FROM patterns p
                    JOIN responses r ON p.intent_tag = r.intent_tag
                    LEFT JOIN vector_store vs ON p.id = vs.pattern_id
                    WHERE p.is_active = 1 
                    AND r.is_active = 1
                    AND (vs.vector_status IS NULL 
                        OR vs.vector_status = 'pending'
                        OR vs.vector_status = 'failed')
                    ORDER BY p.id
                ''')
                patterns = cursor.fetchall()
                
                if patterns:
                    logger.info(f"총 {len(patterns)}개의 패턴 벡터 생성 시작")
                    
                    # 배치 처리를 위한 데이터 준비
                    batch_size = 100
                    batch_data = []
                    
                    for pattern in tqdm(patterns, desc="벡터 생성"):
                        try:
                            # 벡터 생성
                            vector = model.encode(pattern['pattern']).tolist()
                            
                            # 배치 데이터 추가
                            batch_data.append((
                                pattern['id'],
                                json.dumps(vector),
                                pattern['pattern'],
                                pattern['response'],
                                'completed'
                            ))
                            
                            # 배치 크기에 도달하면 DB에 저장
                            if len(batch_data) >= batch_size:
                                cursor.executemany('''
                                    INSERT INTO vector_store 
                                    (pattern_id, vector, pattern_text, response, vector_status)
                                    VALUES (%s, %s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE
                                    vector = VALUES(vector),
                                    pattern_text = VALUES(pattern_text),
                                    response = VALUES(response),
                                    vector_status = VALUES(vector_status)
                                ''', batch_data)
                                conn.commit()
                                batch_data = []
                        
                        except Exception as e:
                            logger.error(f"벡터 생성 실패 (pattern_id: {pattern['id']}): {str(e)}")
                            continue
                    
                    # 남은 배치 데이터 처리
                    if batch_data:
                        cursor.executemany('''
                            INSERT INTO vector_store 
                            (pattern_id, vector, pattern_text, response, vector_status)
                            VALUES (%s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                            vector = VALUES(vector),
                            pattern_text = VALUES(pattern_text),
                            response = VALUES(response),
                            vector_status = VALUES(vector_status)
                        ''', batch_data)
                        conn.commit()
                    
                    logger.info("벡터 처리 완료")
                    return {
                        'status': 'success',
                        'message': f'총 {len(patterns)}개의 패턴 벡터 생성 완료',
                        'total_patterns': len(patterns)
                    }
                else:
                    logger.info("갱신이 필요한 패턴이 없습니다.")
                    return {
                        'status': 'success',
                        'message': '갱신이 필요한 패턴이 없습니다.',
                        'total_patterns': 0
                    }
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"벡터 스토어 초기화 중 오류 발생: {str(e)}")
        return {
            'status': 'error',
            'message': f'벡터 스토어 초기화 실패: {str(e)}',
            'total_patterns': 0
        }

def validate_vector_store():
    """벡터 스토어 상태 검증"""
    logger.info("벡터 스토어 검증 시작")
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 패턴과 벡터 매칭 확인
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_patterns,
                    SUM(CASE WHEN vs.id IS NOT NULL THEN 1 ELSE 0 END) as total_vectors
                FROM patterns p
                LEFT JOIN vector_store vs ON p.id = vs.pattern_id
                WHERE p.is_active = 1
            ''')
            result = cursor.fetchone()
            
            total_patterns = result['total_patterns']
            total_vectors = result['total_vectors']
            
            logger.info(f"총 패턴 수: {total_patterns}")
            logger.info(f"총 벡터 수: {total_vectors}")
            
            if total_patterns != total_vectors:
                logger.warning(f"벡터 누락: {total_patterns - total_vectors}개")
                return False
            
            # 2. 벡터 데이터 무결성 확인
            cursor.execute('''
                SELECT COUNT(*) as invalid_vectors
                FROM vector_store
                WHERE vector IS NULL 
                   OR pattern_text IS NULL 
                   OR response IS NULL
            ''')
            invalid_count = cursor.fetchone()['invalid_vectors']
            
            if invalid_count > 0:
                logger.warning(f"무효한 벡터 데이터: {invalid_count}개")
                return False
            
            logger.info("벡터 스토어 검증 완료: 정상")
            return True
            
    finally:
        conn.close()

def log_vector_update(pattern_id, status, error=None):
    """벡터 업데이트 로그 기록"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO vector_update_logs
                (pattern_id, status, error_message)
                VALUES (%s, %s, %s)
            ''', (pattern_id, status, error))
            conn.commit()
    finally:
        conn.close() 