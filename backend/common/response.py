from flask import jsonify

def make_response(success=True, code="SUCCESS", message="", data=None, error=None, status=200):
    """
    공통 API 응답 생성 함수
    :param success: 성공 여부 (True/False)
    :param code: 응답 코드 (성공/에러/권한 등)
    :param message: 사용자 안내 메시지
    :param data: 실제 데이터 (성공시)
    :param error: 에러 정보 (실패시)
    :param status: HTTP 상태 코드
    :return: Flask Response
    """
    resp = {
        "success": success,
        "code": code,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(resp), status

class ApiResponse:
    @staticmethod
    def success(data=None, message="성공적으로 처리되었습니다.", code="SUCCESS"):
        return make_response(True, code, message, data, None, 200)

    @staticmethod
    def error(code, message, reason=None, status=400):
        return make_response(False, code, message, None, {
            "code": code,
            "reason": reason,
            "message": message
        }, status) 