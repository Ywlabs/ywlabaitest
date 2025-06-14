from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
from database import get_db_connection
from common.logger import setup_logger
from datetime import datetime

logger = setup_logger('employee_info_handler')

def handle(user_message: str, meta: dict, response: str) -> dict:
    """
    직원 정보 조회 핸들러
    - user_message: 사용자 메시지
    - meta: 메타데이터
    - response: 기본 응답 템플릿
    """
    name = extract_employee_name(user_message)
    logger.info(f"[핸들러] 추출된 직원 이름: {name}")
    
    if not name:
        logger.warning("[핸들러] 직원 이름 추출 실패")
        return {
            'response': '직원 이름을 입력해주세요.',
            'type': 'text',
            'timestamp': datetime.now().isoformat()
        }
    
    # 직원 정보 DB 조회
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            logger.debug(f"[핸들러] 직원 DB에서 name={name}으로 정보 조회")
            cursor.execute('''
                SELECT name, position, dept_nm, email, phone 
                FROM employees 
                WHERE name = %s
            ''', (name,))
            employee = cursor.fetchone()
            logger.debug(f"[핸들러] 직원 정보: {employee}")
    finally:
        conn.close()
    
    if not employee:
        logger.warning(f"[핸들러] 직원 정보 없음: {name}")
        return {
            'response': f'죄송합니다. {name}님의 정보를 찾을 수 없습니다.',
            'type': 'text',
            'timestamp': datetime.now().isoformat()
        }
    
    # 직원 정보로 템플릿 채우기
    employee_response = get_employee_info_and_fill_template(name, response)
    logger.info(f"[핸들러] 직원 템플릿 응답: {employee_response}")
    
    return {
        'response': employee_response,
        'type': 'dynamic',
        'timestamp': datetime.now().isoformat(),
        'employee': {
            'name': employee['name'],
            'position': employee['position'],
            'dept_nm': employee['dept_nm'],
            'email': employee['email'],
            'phone': employee['phone']
        },
        'metadata': {
            'domain': meta.get('domain'),
            'category': meta.get('category'),
            'pattern_id': meta.get('pattern_id'),
            'pattern_text': meta.get('pattern_text'),
            'pattern_type': meta.get('pattern_type')
        }
    } 