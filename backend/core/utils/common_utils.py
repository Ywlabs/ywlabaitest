import datetime
import re

# 현재 날짜와 시간을 YYYY-MM-DD HH:MM:SS 문자열로 반환
def get_now_str():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 문자열에서 모든 공백 제거
def remove_whitespace(text):
    return re.sub(r'\s+', '', text)

# 문자열이 숫자로만 이루어져 있는지 확인
def is_numeric(text):
    return text.isdigit()

# 문자열을 카멜케이스로 변환 (예: hello_world → helloWorld)
def to_camel_case(text):
    parts = text.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:]) 