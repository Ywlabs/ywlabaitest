from flask import Blueprint, jsonify
from common.logger import setup_logger
from services.legacy_service import get_weather, get_air_quality

# 로거 설정
logger = setup_logger('legacy_routes')

legacy_bp = Blueprint('legacy', __name__)

@legacy_bp.route('/api/legacy/weather', methods=['GET'])
def get_weather_route():
    """강동구 오늘의 날씨 정보 조회 (route)"""
    try:
        weather = get_weather()
        return jsonify({
            'status': 'success',
            'data': weather
        })
    except Exception as e:
        logger.error(f"날씨 정보 조회 중 오류 발생: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '날씨 정보를 불러오는데 실패했습니다.'
        }), 500

@legacy_bp.route('/api/legacy/air-quality', methods=['GET'])
def get_air_quality_route():
    """강동구 오늘의 대기질 정보 조회 (route)"""
    try:
        air_quality = get_air_quality()
        return jsonify({
            'status': 'success',
            'data': air_quality
        })
    except Exception as e:
        logger.error(f"대기질 정보 조회 중 오류 발생: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '대기질 정보를 불러오는데 실패했습니다.'
        }), 500 