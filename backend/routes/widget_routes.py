from flask import Blueprint, request
from services.widget_service import search_widgets
from common.response import ApiResponse
import logging
from routes import jwt_required  # JWT 인증 데코레이터 import

logger = logging.getLogger(__name__)

widget_bp = Blueprint('widgets', __name__)

@widget_bp.route('/api/widgets/search', methods=['POST'])
@jwt_required  # JWT 인증 필요
def widget_search():
    """
    날씨정보 위젯 검색
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        results = search_widgets(query)
        return ApiResponse.success(data=results, message="위젯 검색 성공")
    except Exception as e:
        logger.error(f"위젯 검색 중 오류 발생: {str(e)}")
        return ApiResponse.error("ERR_SERVER", "위젯 검색 실패", reason=str(e), status=500) 
        logger.error(f"위젯 검색 중 오류 발생: {str(e)}")
        return ApiResponse.error("ERR_SERVER", "위젯 검색 실패", reason=str(e), status=500) 
        logger.error(f"위젯 검색 중 오류 발생: {str(e)}")
        return ApiResponse.error("ERR_SERVER", "위젯 검색 실패", reason=str(e), status=500) 
        logger.error(f"위젯 검색 중 오류 발생: {str(e)}")
        return ApiResponse.error("ERR_SERVER", "위젯 검색 실패", reason=str(e), status=500) 