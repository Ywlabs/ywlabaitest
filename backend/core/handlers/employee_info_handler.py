from services.employee_service import extract_employee_name, get_employee_info_and_fill_template
from database import get_db_connection
from common.logger import setup_logger

logger = setup_logger('employee_info_handler')

def handle_employee_info(user_message, meta, response):
    """
    직원 이름 추출, DB 조회, 템플릿 채우기 등 employee_info intent 후처리
    """
    name = extract_employee_name(user_message)
    logger.info(f"[handle_employee_info] 추출된 직원 이름: {name}")
    employee_response = None
    employee_dict = None
    if name:
        conn2 = get_db_connection()
        try:
            with conn2.cursor() as cursor2:
                logger.debug(f"[handle_employee_info] 직원 DB에서 name={name}으로 정보 조회")
                cursor2.execute('''
                    SELECT name, position, dept_nm, email, phone FROM employees WHERE name = %s
                ''', (name,))
                employee_dict = cursor2.fetchone()
                logger.debug(f"[handle_employee_info] 직원 정보: {employee_dict}")
        finally:
            conn2.close()
        if employee_dict:
            employee_response = get_employee_info_and_fill_template(name, response)
            logger.info(f"[handle_employee_info] 직원 템플릿 응답: {employee_response}")
            return {
                'status': 'success',
                'data': {
                    'response': employee_response,
                    'response_type': 'dynamic',
                    'employee': employee_dict,
                    'route_code': None,
                    'route_name': None,
                    'route_path': None,
                    'route_type': None
                }
            }, meta
        else:
            logger.warning(f"[handle_employee_info] 직원 정보 없음: {name}")
            return {
                'status': 'success',
                'data': {
                    'response': f'죄송합니다. {name}님의 정보를 찾을 수 없습니다.',
                    'response_type': 'text',
                    'route_code': None,
                    'route_name': None,
                    'route_path': None,
                    'route_type': None
                }
            }, meta
    else:
        logger.warning(f"[handle_employee_info] 직원 이름 추출 실패")
        return {
            'status': 'success',
            'data': {
                'response': '직원 이름을 입력해주세요.',
                'response_type': 'text',
                'route_code': None,
                'route_name': None,
                'route_path': None,
                'route_type': None
            }
        }, meta 