from flask import Blueprint, jsonify
from common.logger import setup_logger

# 로거 설정
logger = setup_logger('routes')

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/api/routes', methods=['GET'])
def get_routes():
    """사용 가능한 라우트 목록 조회"""
    try:
        routes = [
            {
                "route_code": "DASHBOARD_WIDGET",
                "name": "대시보드",
                "description": "에너지 사용량 대시보드"
            },
            {
                "route_code": "ORG_CHART",
                "name": "조직도",
                "description": "회사 조직도"
            },
            {
                "route_code": "SALES_WIDGET",
                "name": "매출 현황",
                "description": "매출 현황 위젯"
            }
        ]
        return jsonify({
            'status': 'success',
            'data': routes
        })
    except Exception as e:
        logger.error(f"라우트 목록 조회 중 오류 발생: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '라우트 목록을 불러오는데 실패했습니다.'
        }), 500 