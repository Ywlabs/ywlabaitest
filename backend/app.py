from flask import Flask
from flask_cors import CORS
from routes.chat_routes import chat_bp, routes_bp
from routes.vector_routes import vector_bp
from routes.employee_routes import employee_bp
from routes.legacy_routes import legacy_bp
from routes.sales_routes import sales_bp  # 매출 API 블루프린트 추가
from routes.widget_routes import widget_bp  
from services.vector_service import initialize_vector_store, validate_vector_store
from common.logger import setup_logger
import threading
from services.chroma_service import initialize_chroma_from_docx
from config import Config  # 공통 설정 import

# 로거 설정
logger = setup_logger('app')

def create_app():
    app = Flask(__name__)
    # CORS는 app 단위로만 적용 (Blueprint에는 적용하지 않음)
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    # 블루프린트 등록
    app.register_blueprint(chat_bp)
    app.register_blueprint(vector_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(routes_bp)  # routes API 블루프린트 등록
    app.register_blueprint(legacy_bp)  # legacy API 블루프린트 등록
    app.register_blueprint(sales_bp)   # 매출 API 블루프린트 등록
    app.register_blueprint(widget_bp)  # 위젯 API 블루프린트 등록
    return app

app = create_app()

def initialize_backend():
    """백엔드 초기화 함수"""
    print("\n=== 백엔드 초기화 시작 ===")
    
    # 벡터 스토어 초기화
    print("\n1. 벡터 스토어 초기화 중...")
    result = initialize_vector_store()
    print(f"✓ {result['message']}")
    
    # 벡터 스토어 검증
    print("\n2. 벡터 스토어 검증 중...")
    is_valid = validate_vector_store()
    if is_valid:
        print("✓ 벡터 스토어 검증 완료: 정상")
    else:
        print("⚠ 벡터 스토어 검증 실패: 문제 발견")

    # Chroma DB 초기화 (워드 문서 → 벡터DB)
    print("\n3. Chroma DB 초기화 중...")
    try:
        # config.py의 공통 설정 사용
        initialize_chroma_from_docx(docx_path=Config.POLICY_DOCX_PATH, chroma_dir=Config.CHROMA_DB_DIR)
        print("✓ Chroma DB 초기화 완료: 정상")
    except Exception as e:
        print(f"⚠ Chroma DB 초기화 실패: {e}")
    
    print("\n=== 백엔드 초기화 완료 ===\n")

if __name__ == '__main__':
    initialize_backend()
    app.run(debug=True, port=5000, host='0.0.0.0')  # host를 0.0.0.0으로 변경하여 모든 IP에서 접근 가능하도록 함 