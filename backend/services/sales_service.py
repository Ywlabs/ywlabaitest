from database import get_db_connection
import numpy as np
from sklearn.linear_model import LinearRegression

# 연도별 매출 집계 함수
def get_sales_summary(year):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT SUM(sales) as total_sales, SUM(net_profit) as total_profit
                FROM sales_history
                WHERE year = %s
            """
            cursor.execute(sql, (year,))
            row = cursor.fetchone()
            if not row or not row['total_sales']:
                return {'total_sales': 0, 'total_profit': 0, 'profit_rate': 0}
            profit_rate = row['total_profit'] / row['total_sales'] if row['total_sales'] else 0
            return {
                'total_sales': int(row['total_sales']),
                'total_profit': int(row['total_profit']),
                'profit_rate': round(profit_rate, 4)
            }
    finally:
        conn.close()

# AI 예측(선형회귀 기반) 함수
def predict_sales(target_year):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT year, SUM(sales) as total_sales, SUM(net_profit) as total_profit
                FROM sales_history
                WHERE year >= 2015 AND year <= 2025
                GROUP BY year
                ORDER BY year
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) < 3:
                # 데이터가 부족하면 0 반환
                return {'total_sales': 0, 'total_profit': 0, 'profit_rate': 0}
            X = np.array([[r['year']] for r in rows])
            y_sales = np.array([r['total_sales'] for r in rows])
            y_profit = np.array([r['total_profit'] for r in rows])
            # 선형회귀 모델 학습
            model_sales = LinearRegression().fit(X, y_sales)
            model_profit = LinearRegression().fit(X, y_profit)
            pred_sales = int(model_sales.predict([[target_year]])[0])
            pred_profit = int(model_profit.predict([[target_year]])[0])
            profit_rate = pred_profit / pred_sales if pred_sales else 0
            return {
                'total_sales': pred_sales,
                'total_profit': pred_profit,
                'profit_rate': round(profit_rate, 4)
            }
    finally:
        conn.close() 