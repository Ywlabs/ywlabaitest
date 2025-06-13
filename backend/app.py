from flask import Flask
from flask_cors import CORS
from routes.chat_routes import chat_bp, routes_bp
from routes.employee_routes import employee_bp
from routes.legacy_routes import legacy_bp
from routes.sales_routes import sales_bp  # 매출 API 블루프린트 추가
from routes.widget_routes import widget_bp  
from common.logger import setup_logger
import threading
from services.chroma_service import initialize_rag_collections, initialize_db_collections
from config import Config  # 공통 설정 import
import os
import shutil

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
    app.register_blueprint(employee_bp)
    app.register_blueprint(routes_bp)  # routes API 블루프린트 등록
    app.register_blueprint(legacy_bp)  # legacy API 블루프린트 등록
    app.register_blueprint(sales_bp)   # 매출 API 블루프린트 등록
    app.register_blueprint(widget_bp)  # 위젯 API 블루프린트 등록
    return app

app = create_app()

def initialize_backend():
    """
    백엔드 및 ChromaDB(문서/DB) 일괄 초기화
    - chromadb 폴더가 없으면 자동으로 새로 생성됩니다.
    - 이미 존재하는 경우 기존 데이터를 덮어쓸 수 있습니다.
    - 완전히 새로 생성하려면 chromadb 폴더를 수동으로 삭제 후 서버를 재시작하세요.
    """
    chroma_dir = Config.RAG_CHROMA_DIR
    print("\n=== 백엔드 및 ChromaDB 초기화 시작 ===")
    print(f"[안내] ChromaDB(문서/DB) 벡터DB 경로: {chroma_dir}")
    if os.path.exists(chroma_dir):
        print(f"[경고] chromadb 폴더({chroma_dir})가 이미 존재합니다.")
        answer = input("기존 chromadb 폴더를 삭제하고 새로 생성하시겠습니까? (Y/N): ").strip().lower()
        if answer == 'y':
            try:
                shutil.rmtree(chroma_dir)
                print(f"[완료] chromadb 폴더({chroma_dir})가 삭제되었습니다.")
            except Exception as e:
                print(f"[오류] chromadb 폴더 삭제 실패: {e}")
                print("[중단] 초기화를 진행하지 않습니다.")
                return
        else:
            print("[안내] 기존 chromadb 폴더를 유지하고 초기화를 진행합니다.")
    else:
        print("[안내] chromadb 폴더가 존재하지 않아 새로 생성됩니다.")
    # 1. RAG 문서/이미지 ChromaDB 초기화
    print("1. RAG 문서/이미지 일괄 초기화 중...")
    try:
        initialize_rag_collections()
        print("[완료] RAG 문서/이미지 컬렉션 초기화 완료.")
    except Exception as e:
        print(f"⚠ RAG 문서/이미지 초기화 실패: {e}")
    # 2. DB 기반 ChromaDB 초기화
    print("2. DB 컬렉션 일괄 초기화 중...")
    try:
        initialize_db_collections()
        print("[완료] DB 컬렉션 초기화 완료.")
    except Exception as e:
        print(f"⚠ DB 컬렉션 초기화 실패: {e}")
    print("\n=== 백엔드 및 ChromaDB 초기화 완료 ===\n")

if __name__ == '__main__':
    initialize_backend()
    app.run(debug=True, port=5000, host='0.0.0.0')  # host를 0.0.0.0으로 변경하여 모든 IP에서 접근 가능하도록 함 