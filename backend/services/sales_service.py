from database import get_db_connection
import numpy as np
from sklearn.linear_model import LinearRegression

def get_sales_info_and_fill_template(year: str, response_template: str) -> str:
    """
    매출 정보를 템플릿에 채워서 반환
    - 입력: 
        - year: 연도
        - response_template: 응답 템플릿
    - 출력: 채워진 응답 문자열
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 현재 연도의 매출 정보 조회
            cursor.execute('''
                SELECT 
                    year,
                    SUM(sales) as total_sales,
                    SUM(sales)/12 as monthly_sales
                FROM sales_history 
                WHERE year = %s
                GROUP BY year
            ''', (year,))
            current_sales = cursor.fetchone()
            
            if not current_sales:
                return None
                
            # 전년도 매출 정보 조회
            prev_year = int(year) - 1
            cursor.execute('''
                SELECT SUM(sales) as prev_total_sales
                FROM sales_history 
                WHERE year = %s
                GROUP BY year
            ''', (prev_year,))
            prev_sales = cursor.fetchone()
            
            # 성장률 계산
            if prev_sales and prev_sales['prev_total_sales'] > 0:
                growth_rate = (current_sales['total_sales'] - prev_sales['prev_total_sales']) / prev_sales['prev_total_sales'] * 100
            else:
                growth_rate = 0
            
            # 응답 템플릿 채우기
            response_text = response_template
            response_text = response_text.replace('{year}', str(current_sales['year']))
            response_text = response_text.replace('{sales.year}', str(current_sales['year']))
            response_text = response_text.replace('{sales.total_sales}', format(current_sales['total_sales'], ','))
            response_text = response_text.replace('{sales.monthly_sales}', format(current_sales['monthly_sales'], ','))
            response_text = response_text.replace('{sales.growth_rate}', f"{growth_rate:.1f}%")
            return response_text
            
    finally:
        conn.close()

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