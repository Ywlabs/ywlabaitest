import logging
from langchain.schema import Document
from typing import Dict, Any, Optional

# 로거 설정
logger = logging.getLogger(__name__)

def pattern_to_document(pattern_row: Dict[str, Any]) -> Document:
    """
    패턴+응답 dict를 LangChain Document로 변환 (메타데이터 포함)
    
    Args:
        pattern_row: DB에서 조회한 패턴 데이터
        
    Returns:
        Document: LangChain Document 객체
    """
    # 1. 필수 메타데이터 추출 및 검증
    required_fields = {
        "pattern_id": pattern_row.get("pattern_id"),
        "domain": pattern_row.get("domain"),
        "category": pattern_row.get("category"),
        "similarity_threshold": pattern_row.get("similarity_threshold"),
        "pattern_type": pattern_row.get("pattern_type"),
        "priority": pattern_row.get("priority", 0)
    }
    
    # 필수 필드 누락 체크
    missing_fields = [k for k, v in required_fields.items() if v is None]
    if missing_fields:
        logger.error(f"[ROUTE] 필수 필드 누락: {missing_fields}")
        raise ValueError(f"필수 필드 누락: {missing_fields}")
    
    # 2. 선택적 메타데이터 추출
    optional_fields = {
        "response": pattern_row.get("response", ""),
        "route_code": pattern_row.get("route_code"),
        "route_type": pattern_row.get("route_type"),
        "route_path": pattern_row.get("route_path"),
        "route_name": pattern_row.get("route_name"),
        "response_type": pattern_row.get("response_type"),
        "response_handler": pattern_row.get("response_handler"),
        "description": pattern_row.get("description", ""),
        "response_description": pattern_row.get("response_description", "")
    }
    
    # 3. 메타데이터 로깅
    logger.debug(f"[ROUTE] 패턴 정보: pattern_id={required_fields['pattern_id']}, "
                f"pattern={pattern_row.get('pattern')}, "
                f"domain={required_fields['domain']}, "
                f"category={required_fields['category']}")
    logger.debug(f"[ROUTE] 라우트 정보: route_code={optional_fields['route_code']}, "
                f"route_type={optional_fields['route_type']}, "
                f"route_path={optional_fields['route_path']}")
    
    # 4. Document 생성
    return Document(
        page_content=pattern_row["pattern"],
        metadata={
            # 필수 필드
            **required_fields,
            
            # 선택적 필드 (None 값 제외)
            **{k: v for k, v in optional_fields.items() if v is not None},
            
            # 검색 가중치 계산
            "search_weight": calculate_search_weight(
                domain=required_fields["domain"],
                category=required_fields["category"],
                pattern_type=required_fields["pattern_type"],
                priority=required_fields["priority"]
            )
        }
    )

def calculate_search_weight(domain: str, category: str, pattern_type: str, priority: int) -> float:
    """
    검색 가중치 계산
    
    Args:
        domain: 도메인
        category: 카테고리
        pattern_type: 패턴 타입 (static/dynamic)
        priority: 우선순위
        
    Returns:
        float: 검색 가중치 (0.0 ~ 1.0)
    """
    # 1. 기본 가중치
    weight = 0.5
    
    # 2. 도메인별 가중치 조정
    domain_weights = {
        "회사": 1.0,    # 회사 정보는 높은 가중치
        "인사": 0.9,    # 인사 관련은 높은 가중치
        "매출": 0.8,    # 매출 관련은 중간 가중치
        "데시보드": 0.7, # 데시보드는 중간 가중치
        "ESG": 0.8,     # ESG는 중간 가중치
        "준법": 0.8     # 준법은 중간 가중치
    }
    weight *= domain_weights.get(domain, 0.5)
    
    # 3. 패턴 타입별 가중치 조정
    if pattern_type == "static":
        weight *= 1.2  # 정적 패턴은 가중치 증가
    elif pattern_type == "dynamic":
        weight *= 0.9  # 동적 패턴은 가중치 감소
    
    # 4. 우선순위 반영
    weight *= (1 + priority * 0.1)  # 우선순위가 높을수록 가중치 증가
    
    # 5. 최종 가중치 정규화 (0.0 ~ 1.0)
    return min(max(weight, 0.0), 1.0)
