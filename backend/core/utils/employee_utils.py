import re
from typing import Optional, Dict, Any
from database import get_db_connection

def extract_employee_name(text: str) -> Optional[str]:
    """
    텍스트에서 직원 이름 추출
    - 입력: text (문자열)
    - 출력: 직원 이름 (문자열) 또는 None
    """
    # 한글 이름 패턴 (2~4글자)
    match = re.search(r'([가-힣]{2,4})님', text)
    if match:
        return match.group(1)
    return None

def get_employee_info(name: str) -> Optional[Dict[str, Any]]:
    """
    직원 정보 조회
    - 입력: name (직원 이름)
    - 출력: 직원 정보 (딕셔너리) 또는 None
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT name, position, dept_nm, email, phone
                FROM employee_info 
                WHERE name = %s
            ''', (name,))
            employee = cursor.fetchone()
            if employee:
                return {
                    'name': employee['name'],
                    'position': employee['position'],
                    'dept_nm': employee['dept_nm'],
                    'email': employee['email'],
                    'phone': employee['phone']
                }
    finally:
        conn.close()
    return None 