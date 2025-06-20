from flask import Blueprint
from database import get_db_connection
from common.logger import setup_logger
from services.employee_service import get_employee_list, get_employee_detail
from common.response import ApiResponse

# 로거 설정
logger = setup_logger('employee_routes')

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/api/employee/list', methods=['GET'])
def get_employee_list_route():
    """
    직원 목록 조회 (route)
    """
    try:
        employees = get_employee_list()
        return ApiResponse.success(data=employees, message="직원 목록 조회 성공")
    except Exception as e:
        logger.error(f"직원 정보 조회 중 오류 발생: {str(e)}")
        return ApiResponse.error("ERR_SERVER", "직원 정보를 불러오는데 실패했습니다.", reason=str(e), status=500)

@employee_bp.route('/api/employee/<int:employee_id>', methods=['GET'])
def get_employee_detail_route(employee_id):
    """
    직원 상세 정보 조회 (route)
    """
    try:
        employee = get_employee_detail(employee_id)
        if employee:
            return ApiResponse.success(data=employee, message="직원 상세 정보 조회 성공")
        else:
            return ApiResponse.error("ERR_NOT_FOUND", "해당 직원을 찾을 수 없습니다.", reason="DB에 없음", status=404)
    except Exception as e:
        logger.error(f"직원 상세 정보 조회 중 오류 발생: {str(e)}")
        return ApiResponse.error("ERR_SERVER", "직원 정보를 불러오는데 실패했습니다.", reason=str(e), status=500) 