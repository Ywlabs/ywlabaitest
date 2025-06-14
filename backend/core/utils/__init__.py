"""
유틸리티 함수 모음
- date_utils: 날짜 관련 유틸리티
- employee_utils: 직원 정보 관련 유틸리티
"""

import importlib
from typing import Callable, Any

from .date_utils import extract_year, get_current_year, format_date
from .employee_utils import extract_employee_name

__all__ = [
    'extract_year',
    'get_current_year',
    'format_date',
    'extract_employee_name',
    'get_func_from_str'
]

def get_func_from_str(func_path: str) -> Callable:
    """
    문자열로 된 함수 경로에서 함수 객체 반환
    - 입력: func_path (예: 'module.submodule.function')
    - 출력: 함수 객체
    """
    module_path, func_name = func_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name) 