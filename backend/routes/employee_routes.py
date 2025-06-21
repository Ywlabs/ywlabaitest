from flask import Blueprint
from database import get_db_connection
from common.logger import setup_logger
from services.employee_service import get_employee_list, get_employee_detail
from common.response import ApiResponse
from routes import jwt_required  # JWT 인증 데코레이터 import

# 로거 설정
logger = setup_logger('employee_routes')

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/api/employee/list', methods=['GET'])
@jwt_required
def employee_list():
    """직원 목록 조회"""
    try:
        employees = get_employee_list()
        return ApiResponse.success(data=employees, message="직원 목록 조회 성공")
    except Exception as e:
        logger.error(f"직원 목록 조회 중 오류 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "직원 목록 조회 실패", reason=str(e), status=500)

@employee_bp.route('/api/employee/info', methods=['GET'])
@jwt_required  # JWT 인증 필요
def get_employee_info():
    """
    직원 정보 조회
    """
    try:
        logger.info("직원 정보 조회 시작")
        employee_info = get_employee_detail()
        logger.info("직원 정보 조회 완료")
        return ApiResponse.success(data=employee_info, message="직원 정보 조회 성공")
    except Exception as e:
        logger.error(f"직원 정보 조회 중 오류 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "직원 정보 조회 실패", reason=str(e), status=500)

@employee_bp.route('/api/employee/attendance', methods=['GET'])
@jwt_required  # JWT 인증 필요
def get_attendance_info():
    """
    출근 정보 조회
    """
    try:
        logger.info("출근 정보 조회 시작")
        attendance_info = get_attendance_data()
        logger.info("출근 정보 조회 완료")
        return ApiResponse.success(data=attendance_info, message="출근 정보 조회 성공")
    except Exception as e:
        logger.error(f"출근 정보 조회 중 오류 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "출근 정보 조회 실패", reason=str(e), status=500) 