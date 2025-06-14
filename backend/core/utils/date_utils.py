import re
from typing import Optional
from datetime import datetime

def extract_year(text: str) -> Optional[str]:
    """
    텍스트에서 연도 추출
    - 입력: text (문자열)
    - 출력: 연도 (문자열) 또는 None
    """
    match = re.search(r'(20[0-9]{2})년', text)
    if match:
        return match.group(1)
    return None

def get_current_year() -> str:
    """
    현재 연도 반환
    - 출력: 현재 연도 (문자열)
    """
    return str(datetime.now().year)

def format_date(date_str: str, input_format: str = '%Y-%m-%d', output_format: str = '%Y년 %m월 %d일') -> str:
    """
    날짜 문자열 포맷 변환
    - 입력: 
        - date_str: 날짜 문자열
        - input_format: 입력 포맷
        - output_format: 출력 포맷
    - 출력: 포맷된 날짜 문자열
    """
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str 