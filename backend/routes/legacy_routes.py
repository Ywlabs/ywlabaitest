from flask import Blueprint, jsonify, Response
from common.logger import setup_logger
from services.environment_service import EnvironmentService
from common.response import ApiResponse
import json
import logging
from routes import jwt_required  # JWT 인증 데코레이터 import

# 로거 설정
logger = setup_logger('legacy_routes')

# Blueprint 생성
legacy_bp = Blueprint('legacy', __name__)

@legacy_bp.route('/api/environment/current', methods=['GET'])
@jwt_required  # JWT 인증 필요
def get_environment_current():
    """현재 환경 정보 조회"""
    try:
        logger.info("[API] 현재 환경 정보 조회 요청 시작")
        
        # 환경 정보 서비스 인스턴스 생성
        environment_service = EnvironmentService()
        logger.info("[API] EnvironmentService 인스턴스 생성 성공")
        
        # 최신 환경 정보 조회
        env = environment_service.get_latest_environment()
        logger.info(f"[API] get_latest_environment() 결과: {env}")
        
        # 환경 정보가 없는 경우 처리
        if not env:
            logger.warning("[API] 환경 정보가 없습니다. 기본값으로 응답합니다.")
            data = {
                'weather': {
                    'temp': 0,
                    'main': 'Unknown',
                    'description': '데이터 없음'
                },
                'air_quality': {
                    'pm10': '알수없음',
                    'pm25': '알수없음',
                    'khai_grade': '-'
                },
                'timestamp': None
            }
            return ApiResponse.success(data=data, message="환경 정보가 없어 기본값으로 응답합니다.")
        
        # 응답 데이터 구성
        data = {
            'weather': {
                'temp': env['temp'],
                'main': env['main'],
                'description': env['weather_desc']
            },
            'air_quality': {
                'pm10': env['pm10'],
                'pm25': env['pm25'],
                'khai_grade': env['khai_grade']
            },
            'timestamp': env['timestamp']
        }
        logger.info(f"[API] 응답 데이터 구성 완료: {data}")
        return ApiResponse.success(data=data, message="환경 정보 조회 성공")
        
    except Exception as e:
        logger.error(f"환경 정보 조회 중 예외 발생: {str(e)}", exc_info=True)
        return ApiResponse.error("ERR_SERVER", "환경 정보 조회 실패", reason=str(e), status=500)

@legacy_bp.route('/api/environment/stream', methods=['GET'])
@jwt_required
def get_environment_stream():
    """SSE 스트림 연결"""
    logger.info("[API] SSE 스트림 연결 요청: /environment/stream")
    
    # 환경 정보 서비스 인스턴스 생성
    environment_service = EnvironmentService()
    
    def generate():
        try:
            # 클라이언트 연결 시 초기 데이터 전송
            env = environment_service.get_latest_environment()
            if env:
                data = {
                    'status': 'success',
                    'data': env
                }
                yield f"data: {json.dumps(data)}\n\n"
            else:
                # 초기 데이터가 없는 경우 에러 메시지 전송
                error_data = {
                    'status': 'error',
                    'message': '환경 정보를 찾을 수 없습니다.'
                }
                yield f"data: {json.dumps(error_data)}\n\n"

            # 클라이언트를 SSE 클라이언트 목록에 추가
            environment_service.add_sse_client(generate)
            logger.info("[API] SSE 클라이언트 연결됨")

            # 연결 유지 및 주기적 데이터 전송
            while True:
                try:
                    # 30초마다 ping 메시지 전송
                    yield "data: {\"type\": \"ping\"}\n\n"
                    yield "data: {\"type\": \"ping\"}\n\n"
                except Exception as e:
                    logger.error(f"SSE 데이터 전송 중 오류 발생: {str(e)}")
                    error_data = {
                        'status': 'error',
                        'message': '데이터 전송 중 오류가 발생했습니다.'
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                    break

        except Exception as e:
            logger.error(f"SSE 스트림 생성 중 오류 발생: {str(e)}")
            error_data = {
                'status': 'error',
                'message': '스트림 연결 중 오류가 발생했습니다.'
            }
            yield f"data: {json.dumps(error_data)}\n\n"
        finally:
            # 클라이언트 연결 종료 시 제거
            environment_service.remove_sse_client(generate)
            logger.error(f"SSE 클라이언트 연결 종료")

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
            'Access-Control-Allow-Origin': '*',  # CORS 허용
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',  # Authorization 헤더 허용
            'Access-Control-Allow-Methods': 'GET, OPTIONS',  # HTTP 메서드 허용
            'Access-Control-Allow-Credentials': 'true'  # Credentials 허용
        }
    ) 

# @legacy_bp.route('/api/legacy/employees', methods=['GET'])
# @jwt_required  # JWT 인증 필요
# def get_legacy_employees():
#     """
#     레거시 직원 목록 조회
#     """
#     try:
#         logger.info("레거시 직원 목록 조회 시작")
#         employees = get_legacy_employee_list()
#         logger.info(f"레거시 직원 목록 조회 완료: {len(employees)}명")
#         return ApiResponse.success(data=employees, message="레거시 직원 목록 조회 성공")
#     except Exception as e:
#         logger.error(f"레거시 직원 목록 조회 중 오류 발생: {str(e)}", exc_info=True)
#         return ApiResponse.error("ERR_SERVER", "레거시 직원 목록 조회 실패", reason=str(e), status=500)

# @legacy_bp.route('/api/legacy/employee/<int:employee_id>', methods=['GET'])
# @jwt_required  # JWT 인증 필요
# def get_legacy_employee_detail(employee_id):
#     """
#     레거시 직원 상세 정보 조회
#     """
#     try:
#         logger.info(f"레거시 직원 상세 정보 조회 시작: employee_id={employee_id}")
#         employee = get_legacy_employee_detail_data(employee_id)
#         if not employee:
#             logger.warning(f"레거시 직원을 찾을 수 없음: employee_id={employee_id}")
#             return ApiResponse.error("ERR_NOT_FOUND", "직원을 찾을 수 없습니다.", reason=f"employee_id: {employee_id}", status=404)
#         logger.info(f"레거시 직원 상세 정보 조회 완료: employee_id={employee_id}")
#         return ApiResponse.success(data=employee, message="레거시 직원 상세 정보 조회 성공")
#     except Exception as e:
#         logger.error(f"레거시 직원 상세 정보 조회 중 오류 발생: employee_id={employee_id}, error={str(e)}", exc_info=True)
#         return ApiResponse.error("ERR_SERVER", "레거시 직원 상세 정보 조회 실패", reason=str(e), status=500) 
