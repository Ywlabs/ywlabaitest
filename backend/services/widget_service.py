from services.chat_service import get_ai_response
from core.converters.widget_converter import widget_to_document
from common.logger import setup_logger
from database import get_db_connection
import re

logger = setup_logger('widget_service')

def get_all_widgets():
    """활성화된 전체 위젯 목록 반환"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT id, name, description, category, component_name, thumbnail_url
                FROM widgets
                WHERE is_active = 1
                ORDER BY id ASC
            ''')
            results = cursor.fetchall()
            logger.info(f"[search_widgets] 전체 위젯 반환: {len(results)}")
            return results
    finally:
        conn.close()

def is_all_widget_query(query):
    """한글 쿼리에서 공백/특수문자 제거 후 전체 위젯 요청 패턴 유연하게 인식"""
    norm = re.sub(r'\s+', '', query)
    norm = re.sub(r'[\W_]+', '', norm)  # 한글, 영문, 숫자만 남김
    patterns = [
        '전체위젯', '모든위젯', '지원하는위젯', '위젯정보'
    ]
    for pat in patterns:
        if pat in norm:
            return True
    return False

def get_widgets_by_ids(widget_ids):
    if not widget_ids:
        return []
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            format_strings = ','.join(['%s'] * len(widget_ids))
            cursor.execute(f'''
                SELECT id, name, description, category, component_name, thumbnail_url
                FROM widgets
                WHERE is_active = 1 AND id IN ({format_strings})
                ORDER BY FIELD(id, {format_strings})
            ''', tuple(widget_ids)*2)
            widgets = cursor.fetchall()
            return widgets
    finally:
        conn.close()

def search_widgets(query):
    """
    위젯 검색 함수
    - 2024-06-14 기준: widget_collection에서만 검색
    - 절대 다른 컬렉션(chatbot_collection, policy_collection 등)을 사용하지 말 것!
    """
    try:
        logger.info(f"[search_widgets] 입력 쿼리: {query}")
        if is_all_widget_query(query):
            return get_all_widgets()
        # DB_CHROMA_COLLECTIONS 기반 벡터 검색 (widget_collection 사용)
        from services.chroma_service import search_similar_in_collection
        docs = search_similar_in_collection("widget_collection", query, top_k=10)
        widget_ids = [doc.metadata["widget_id"] for doc in docs]
        logger.info(f"[search_widgets] chroma_service 기반 widget_ids: {widget_ids}")
        if widget_ids:
            return get_widgets_by_ids(widget_ids)
        return get_all_widgets()
    except Exception as e:
        logger.error(f"search_widgets error: {str(e)}")
        return []

def upsert_widget(widget):
    # DB에 저장 (ON DUPLICATE KEY UPDATE)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO widgets (id, name, description, category, component_name, thumbnail_url, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name=VALUES(name),
                    description=VALUES(description),
                    category=VALUES(category),
                    component_name=VALUES(component_name),
                    thumbnail_url=VALUES(thumbnail_url),
                    is_active=VALUES(is_active)
            ''', (
                widget['id'],
                widget['name'],
                widget['description'],
                widget['category'],
                widget['component_name'],
                widget['thumbnail_url'],
                widget.get('is_active', 1)
            ))
            conn.commit()
    finally:
        conn.close()
    # 벡터스토어 동기화 코드 제거 (chroma_service.py에서 일괄 처리) 