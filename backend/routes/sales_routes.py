from flask import Blueprint
from services.sales_service import get_sales_summary, predict_sales
from common.response import ApiResponse
import logging

sales_bp = Blueprint('sales', __name__)

# 연도별 매출 및 AI 예측 결과를 반환하는 API
@sales_bp.route('/api/sales/<int:year>', methods=['GET'])
def get_sales(year):
    """
    연도별 실제 매출 집계 및 AI 예측 결과 반환
    - year: 요청 연도 (int)
    """
    try:
        summary = get_sales_summary(year)
        ai_predict = predict_sales(year)
        data = {
            "year": year,
            "total_sales": summary['total_sales'],
            "profit_rate": summary['profit_rate'],
            "ai_predict": {
                "total_sales": ai_predict['total_sales'],
                "profit_rate": ai_predict['profit_rate']
            }
        }
        return ApiResponse.success(data=data, message="매출 데이터 조회 성공")
    except Exception as e:
        logging.error(f"매출 데이터 조회 중 오류 발생: {str(e)}")
        return ApiResponse.error("ERR_SERVER", "매출 데이터 조회 실패", reason=str(e), status=500) 