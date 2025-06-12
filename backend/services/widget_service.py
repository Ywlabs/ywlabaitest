from services.chat_service import get_ai_response
from services.vector_service import model, find_similar_widget, vector_store
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

def search_widgets(query):
    try:
        logger.info(f"[search_widgets] 입력 쿼리: {query}")
        if is_all_widget_query(query):
            return get_all_widgets()

        # 콤마로 분리된 다중 키워드 처리
        keywords = [q.strip() for q in query.split(',') if q.strip()]
        all_widget_ids = set()
        for kw in keywords:
            message_vector = model.encode(kw)
            similar_results = find_similar_widget(message_vector, top_k=10)
            if similar_results:
                if isinstance(similar_results, dict):
                    similar_results = [similar_results]
                for r in similar_results:
                    if r.get('widget_id'):
                        all_widget_ids.add(r['widget_id'])
        logger.info(f"[search_widgets] 다중 키워드 기반 widget_ids: {all_widget_ids}")
        if all_widget_ids:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    format_strings = ','.join(['%s'] * len(all_widget_ids))
                    cursor.execute(f'''
                        SELECT id, name, description, category, component_name, thumbnail_url
                        FROM widgets
                        WHERE is_active = 1 AND id IN ({format_strings})
                        ORDER BY FIELD(id, {format_strings})
                    ''', tuple(all_widget_ids)*2)
                    widgets = cursor.fetchall()
                    logger.info(f"[search_widgets] 다중 키워드 기반 최종 반환 개수: {len(widgets)}")
                    if widgets:
                        return widgets
            finally:
                conn.close()
        # 결과 없으면 전체 위젯 반환
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
    # 임베딩 생성 및 vector_store에 저장
    embedding = get_embedding(widget['description'] + widget['name'])
    vector_store.upsert(widget['id'], embedding)

def get_embedding(text):
    """입력 텍스트를 임베딩 벡터로 변환"""
    return model.encode(text).tolist() 