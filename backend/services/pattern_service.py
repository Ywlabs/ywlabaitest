from langchain.schema import Document
from database import get_db_connection

# 패턴+응답 전체 조회 함수

def get_all_patterns():
    """DB에서 활성화된 패턴+응답+route 전체를 반환 (dict 리스트)"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT p.id as pattern_id, p.pattern as pattern_text, 
                       p.intent_tag,
                       r.response, r.route_code,
                       p.pattern_type, p.is_active,
                       r.response_type, r.is_active as response_active,
                       rt.route_name, rt.route_path, rt.route_type
                FROM patterns p
                JOIN responses r ON p.response_id = r.id
                LEFT JOIN routes rt ON r.route_code = rt.route_code
                WHERE p.is_active = 1 AND r.is_active = 1
            ''')
            return cursor.fetchall()
    finally:
        conn.close()

# 패턴+응답을 LangChain Document로 변환

def pattern_to_document(pattern_row):
    """패턴+응답 dict를 LangChain Document로 변환 (메타데이터 포함)"""
    return Document(
        page_content=pattern_row["pattern_text"],
        metadata={
            "pattern_id": pattern_row["pattern_id"],
            "intent_tag": pattern_row.get("intent_tag"),
            "response": pattern_row["response"],
            "route_code": pattern_row["route_code"],
            "pattern_type": pattern_row["pattern_type"],
            "response_type": pattern_row["response_type"],
            "route_name": pattern_row.get("route_name"),
            "route_path": pattern_row.get("route_path"),
            "route_type": pattern_row.get("route_type"),
        }
    ) 