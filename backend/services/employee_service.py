import re
from database import get_db_connection

def extract_employee_name(user_message):
    """
    Extract employee name from user message for both static and dynamic patterns.
    Returns the name string or None if not found.
    """
    # 동적 패턴: {name} 정보, {name}씨 정보 등
    match = re.search(r'(\b[가-힣]{2,4})[\s씨]*정보', user_message)
    if match:
        return match.group(1)
    # 정적 패턴: 영우랩스 조정현, 조정현 대표 등
    # 패턴에서 이름 부분만 추출
    name = user_message
    for pat in ['영우랩스 ', '대표', '이사', '님', '정보', '과장','차장','사원','부장','대표이사','대표님','대표님']:
        name = name.replace(pat, '')
    name = name.strip()
    if name:
        return name
    return None

def get_employee_info_and_fill_template(name, response_template):
    """
    Given a name and a response template, fetch employee info from DB and fill the template.
    Returns the filled response string, or None if not found.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT name, position, dept_nm, email, phone FROM employees WHERE name = %s
            ''', (name,))
            employee = cursor.fetchone()
        if employee:
            response_text = response_template
            response_text = response_text.replace('{employee.name}', employee['name'])
            response_text = response_text.replace('{employee.position}', employee['position'] or '')
            response_text = response_text.replace('{employee.dept_nm}', employee['dept_nm'] or '')
            response_text = response_text.replace('{employee.email}', employee['email'] or '')
            response_text = response_text.replace('{employee.phone}', employee['phone'] or '')
            return response_text
        else:
            return None
    finally:
        conn.close()

def get_employee_list():
    """
    Return a list of all employees as dicts.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    id,
                    name,
                    email,
                    phone,
                    position,
                    dept_nm,
                    sns,
                    created_at,
                    updated_at
                FROM employees 
                ORDER BY dept_nm, position, name
            ''')
            employees = cursor.fetchall()
            return [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'email': item['email'],
                    'phone': item['phone'],
                    'position': item['position'],
                    'dept_nm': item['dept_nm'],
                    'sns': item['sns'],
                    'created_at': item['created_at'].isoformat() if item['created_at'] else None,
                    'updated_at': item['updated_at'].isoformat() if item['updated_at'] else None
                }
                for item in employees
            ]
    finally:
        conn.close()

def get_employee_detail(employee_id):
    """
    Return a single employee dict by id, or None if not found.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    id,
                    name,
                    email,
                    phone,
                    position,
                    dept_nm,
                    sns,
                    created_at,
                    updated_at
                FROM employees 
                WHERE id = %s
            ''', (employee_id,))
            employee = cursor.fetchone()
        if employee:
            return {
                'id': employee['id'],
                'name': employee['name'],
                'email': employee['email'],
                'phone': employee['phone'],
                'position': employee['position'],
                'dept_nm': employee['dept_nm'],
                'sns': employee['sns'],
                'created_at': employee['created_at'].isoformat() if employee['created_at'] else None,
                'updated_at': employee['updated_at'].isoformat() if employee['updated_at'] else None
            }
        else:
            return None
    finally:
        conn.close() 