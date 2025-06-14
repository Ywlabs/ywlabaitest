import logging
from typing import List, Dict, Any
from langchain.schema import Document
from database import get_db_connection
from core.converters.pattern_converter import pattern_to_document

# 로거 설정
logger = logging.getLogger(__name__)

# 패턴+응답 전체 조회 함수

def get_all_patterns():
    """전체 패턴 목록 반환"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
               SELECT 
                    p.id as pattern_id,
                    p.pattern,
                    p.domain,
                    p.category,
                    p.similarity_threshold,
                    p.pattern_type,
                    p.priority,
                    p.description,
                    p.response_handler,
                    r.id as response_id,
                    r.response,
                    r.response_type,
                    r.route_code,
                    r.description as response_description,
                    rt.route_type,
                    rt.route_path,
                    rt.route_name 
                FROM patterns p
                LEFT JOIN patterns_responses pr ON p.id = pr.pattern_id AND pr.is_active = 1
                LEFT JOIN responses r ON pr.response_id = r.id AND r.is_active = 1
                LEFT JOIN routes rt ON r.route_code = rt.route_code AND rt.is_active = 1
                WHERE p.is_active = 1
                ORDER BY p.priority DESC, p.id ASC
            ''')
            results = cursor.fetchall()
            
            # 라우트 정보 로깅
            for row in results:
                if row.get('route_code') and not row.get('route_type'):
                    logger.warning(f"[get_all_patterns] 라우트 정보 누락: route_code={row.get('route_code')}")
            
            logger.info(f"[get_all_patterns] 전체 패턴 반환: {len(results)}")
            return results
    finally:
        conn.close()

class PatternService:
    """패턴 기반 응답 서비스"""
    
    def __init__(self):
        logger.info("[PATTERN] PatternService 초기화 시작")
        self.patterns = self.load_patterns()  # 초기화 시점에 호출
        logger.info("[PATTERN] PatternService 초기화 완료")
        
    def load_patterns(self):
        """DB에서 패턴 데이터 로드"""
        logger.info("[PATTERN] load_patterns 시작")
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # SQL 쿼리 실행
                    cursor.execute("""
                        SELECT p.*, r.route_type, r.route_path, r.route_name 
                        FROM patterns p 
                        LEFT JOIN routes r ON p.route_code = r.route_code
                    """)
                    patterns = cursor.fetchall()
                    logger.info(f"[PATTERN] DB에서 {len(patterns)}개의 패턴 로드됨")
                    
                    # 각 패턴을 Document로 변환
                    documents = [pattern_to_document(pattern) for pattern in patterns]
                    logger.info(f"[PATTERN] {len(documents)}개의 Document 생성됨")
                    return documents
        except Exception as e:
            logger.error(f"[PATTERN] 패턴 로드 중 오류 발생: {str(e)}")
            return []
        
    def get_all_patterns(self):
        """전체 패턴 반환"""
        logger.info(f"[get_all_patterns] 전체 패턴 반환: {len(self.patterns)}")
        return self.patterns 