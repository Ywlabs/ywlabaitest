from flask import Blueprint, request, jsonify
from services.sales_service import get_sales_summary, predict_sales

sales_bp = Blueprint('sales', __name__)

# 연도별 매출 및 AI 예측 결과를 반환하는 API
@sales_bp.route('/api/sales/<int:year>', methods=['GET'])
def get_sales(year):
    """
    연도별 실제 매출 집계 및 AI 예측 결과를 반환
    - year: 요청 연도 (int)
    """
    try:
        summary = get_sales_summary(year)
        ai_predict = predict_sales(year)
        return jsonify({
            "status": "success",
            "data": {
                "year": year,
                "total_sales": summary['total_sales'],
                "profit_rate": summary['profit_rate'],
                "ai_predict": {
                    "total_sales": ai_predict['total_sales'],
                    "profit_rate": ai_predict['profit_rate']
                }
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500 