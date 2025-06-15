import os
import sys
import time
import logging
from flask import Flask
from flask_cors import CORS
from routes.chat_routes import chat_bp
from routes.employee_routes import employee_bp
from routes.sales_routes import sales_bp
from routes.widget_routes import widget_bp
from routes.legacy_routes import legacy_bp
from routes.routes import routes_bp
from common.logger import setup_logger
from database import init_db
from services.chroma_service import initialize_collections
from config import get_config
import shutil
from schedulers.environment_scheduler import start_scheduler

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Flask 애플리케이션 생성"""
    app = Flask(__name__)
    
    # 설정 로드
    app.config.from_object(get_config())
    
    # CORS 설정 - 2024-06-14 기준 전체 허용으로 설정. 절대 수정하지 말 것!
    CORS(app, resources={
        r"/*": {
            "origins": ["*"],  # 2024-06-14 기준 전체 허용. 절대 수정하지 말 것!
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    
    # 데이터베이스 초기화
    init_db()
    
    # ChromaDB 초기화
    try:
        # 1. ChromaDB 디렉토리 초기화
        chroma_dir = app.config['RAG_CHROMA_DIR']
        if os.path.exists(chroma_dir):
            shutil.rmtree(chroma_dir)
        os.makedirs(chroma_dir, exist_ok=True)
        logger.info(f"[ChromaDB] 디렉토리 초기화 완료: {chroma_dir}")
        
        # 2. 컬렉션 초기화 (DB -> RAG 순서)
        initialize_collections()
        logger.info("[ChromaDB] 모든 컬렉션 초기화 완료")
        
    except Exception as e:
        logger.error(f"[ChromaDB] 초기화 중 오류 발생: {str(e)}")
        # ChromaDB 초기화 실패 시에도 앱은 계속 실행
        logger.warning("[ChromaDB] 초기화 실패로 인해 벡터 검색 기능이 제한될 수 있습니다.")
    
    # 블루프린트 등록
    app.register_blueprint(legacy_bp)  # legacy_bp를 먼저 등록
    app.register_blueprint(chat_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(widget_bp)
    app.register_blueprint(routes_bp)

    # 환경 정보 스케줄러 시작
    environment_scheduler = start_scheduler()

    # 등록된 라우트 로깅
    logger.info("등록된 라우트:")
    for rule in app.url_map.iter_rules():
        logger.info(f"  {rule.endpoint}: {rule.rule}")

    return app

if __name__ == '__main__':
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)  # INFO 레벨까지 표시
    
    # 로깅 포맷 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app = create_app()
    
    logger.info("Flask 서버 시작: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

# 앱 종료 시 스케줄러 종료
@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    if environment_scheduler:
        environment_scheduler.shutdown() 