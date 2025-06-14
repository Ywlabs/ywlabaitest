from core.utils.date_utils import extract_year
from services.sales_service import get_sales_info_and_fill_template
from database import get_db_connection
from common.logger import setup_logger
from datetime import datetime

logger = setup_logger('sales_status_handler')

def handle(user_message: str, meta: dict, response: str) -> dict:
    """
    매출 현황 조회 핸들러
    - user_message: 사용자 메시지
    - meta: 메타데이터
    - response: 기본 응답 템플릿
    """
    year = extract_year(user_message)
    logger.info(f"[핸들러] 추출된 연도: {year}")
    
    if not year:
        logger.warning("[핸들러] 연도 추출 실패")
        return {
            'response': '연도를 입력해주세요. (예: 2024년 매출 현황)',
            'response_type': 'none',
            'timestamp': datetime.now().isoformat()
        }
    
    # 매출 정보 DB 조회
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            logger.debug(f"[핸들러] 매출 DB에서 year={year}으로 정보 조회")
            # 현재 연도의 매출 정보 조회
            cursor.execute('''
                SELECT 
                    year,
                    SUM(sales) as total_sales,
                    SUM(sales)/12 as monthly_sales
                FROM sales_history 
                WHERE year = %s
                GROUP BY year
            ''', (year,))
            current_sales = cursor.fetchone()
            logger.debug(f"[핸들러] 현재 연도 매출 정보: {current_sales}")
            
            if not current_sales:
                logger.warning(f"[핸들러] 매출 정보 없음: {year}년")
                return {
                    'response': f'죄송합니다. {year}년 매출 정보를 찾을 수 없습니다.',
                    'response_type': 'none',
                    'timestamp': datetime.now().isoformat()
                }
            
            # 전년도 매출 정보 조회
            prev_year = int(year) - 1
            cursor.execute('''
                SELECT SUM(sales) as prev_total_sales
                FROM sales_history 
                WHERE year = %s
                GROUP BY year
            ''', (prev_year,))
            prev_sales = cursor.fetchone()
            logger.debug(f"[핸들러] 전년도 매출 정보: {prev_sales}")
            
            # 성장률 계산
            if prev_sales and prev_sales['prev_total_sales'] > 0:
                growth_rate = (current_sales['total_sales'] - prev_sales['prev_total_sales']) / prev_sales['prev_total_sales'] * 100
            else:
                growth_rate = 0
            
            # 매출 정보로 템플릿 채우기
            sales_response = get_sales_info_and_fill_template(year, response)
            logger.info(f"[핸들러] 매출 템플릿 응답: {sales_response}")
            
            return {
                'response': sales_response,
                'response_type': meta.get('response_type'),
                'timestamp': datetime.now().isoformat(),
                'route_code': meta.get('route_code',''),
                'route_type': meta.get('route_type',''),
                'route_path': meta.get('route_path',''),
                'route_name': meta.get('route_name',''),
                'metadata': {
                    'domain': meta.get('domain',''),
                    'category': meta.get('category',''),
                    'pattern_id': meta.get('pattern_id',''),
                    'pattern_text': meta.get('pattern_text',''),
                    'pattern_type': meta.get('pattern_type','')
                },
                'resdata': {
                    'sales': {
                        'year': current_sales['year'],
                        'total_sales': current_sales['total_sales'],
                        'monthly_sales': current_sales['monthly_sales'],
                        'growth_rate': growth_rate
                    }
                }
            }
    finally:
        conn.close() 