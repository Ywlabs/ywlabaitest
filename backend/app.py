import sys
import time
import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes.chat_routes import chat_bp
from routes.employee_routes import employee_bp
from routes.sales_routes import sales_bp
from routes.widget_routes import widget_bp
from routes.legacy_routes import legacy_bp
from routes.auth_routes import auth_bp
from common.logger import setup_logger
from database import init_db
from services.chroma_service import initialize_collections
from config import get_config
import shutil
from schedulers.environment_scheduler import start_scheduler
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# 로거 가져오기
logger = logging.getLogger(__name__)

# 배포 버전 정보
DEPLOY_VERSION = "2025-06-21-v1.0.0"
DEPLOY_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def setup_logging():
    """로깅 설정 함수 - 앱 생성 전에 호출"""
    # 환경별 설정 로드
    config = get_config()
    
    # 로그 디렉토리 설정 (환경별로 다름)
    log_dir = config.LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    
    # 로그 파일 경로들
    app_log_file = os.path.join(log_dir, 'app.log')
    error_log_file = os.path.join(log_dir, 'error.log')
    access_log_file = os.path.join(log_dir, 'access.log')
    
    # 로깅 포맷 설정
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    access_format = '%(asctime)s - %(remote_addr)s - %(method)s %(url)s - %(status)s'
    
    # 애플리케이션 로그 핸들러
    app_handler = RotatingFileHandler(
        app_log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    app_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    app_handler.setFormatter(logging.Formatter(log_format))
    
    # 에러 로그 핸들러
    error_handler = RotatingFileHandler(
        error_log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format))
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # 기존 핸들러 제거 (중복 방지)
    print(f"[DEBUG] 기존 루트 로거 핸들러 수: {len(root_logger.handlers)}")
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        print(f"[DEBUG] 루트 로거 핸들러 제거됨: {type(handler).__name__}")
    
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
    print(f"[DEBUG] 루트 로거 핸들러 추가 완료: {len(root_logger.handlers)}개")
    
    # Werkzeug 로거 설정 (Flask 내부 로그)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # 기존 핸들러 제거 (중복 방지)
    print(f"[DEBUG] 기존 Werkzeug 로거 핸들러 수: {len(werkzeug_logger.handlers)}")
    for handler in werkzeug_logger.handlers[:]:
        werkzeug_logger.removeHandler(handler)
        print(f"[DEBUG] Werkzeug 로거 핸들러 제거됨: {type(handler).__name__}")
    
    werkzeug_logger.addHandler(app_handler)
    werkzeug_logger.addHandler(error_handler)
    werkzeug_logger.addHandler(console_handler)
    print(f"[DEBUG] Werkzeug 로거 핸들러 추가 완료: {len(werkzeug_logger.handlers)}개")
    
    return app_log_file, error_log_file

def create_app():
    """Flask 애플리케이션 팩토리 함수"""
    # 로깅 설정 초기화 (가장 먼저 호출)
    app_log_file, error_log_file = setup_logging()
    
    # 로거 가져오기
    logger = logging.getLogger(__name__)
    
    # 환경별 설정 로드
    config = get_config()
    
    # 배포 확인용 로그 (앱 생성 시 출력)
    logger.info(f"✅ [DEPLOY] 앱 생성 시작 - 버전: {DEPLOY_VERSION}")
    logger.info(f"✅ [DEPLOY] 배포 시간: {DEPLOY_TIMESTAMP}")
    logger.info(f"✅ [DEPLOY] 환경: {config.profile}")
    logger.info(f"✅ [DEPLOY] 로그 디렉토리: {config.LOG_DIR}")
    logger.info(f"✅ [DEPLOY] 로그 파일: {app_log_file}")

    # 데이터베이스 초기화
    init_db()
    
    # Frontend 빌드 결과물 경로 설정
    static_folder = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
    
    # 대안 경로들 시도
    alternative_paths = [
        static_folder,  # 기본 경로 (backend/frontend/dist)
        '/app/frontend/dist',  # 절대 경로
        os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'),  # 상위 경로
        os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist'),  # 상위 상위 경로
    ]
    
    # 사용 가능한 경로 찾기
    for path in alternative_paths:
        if os.path.exists(path):
            static_folder = path
            logger.info(f"[DEBUG] 사용할 static_folder 경로: {static_folder}")
            break
    else:
        logger.warning(f"[DEBUG] static_folder를 찾을 수 없음. 시도한 경로들: {alternative_paths}")
        static_folder = alternative_paths[0]  # 기본값 사용
    
    # Flask 앱 생성 (한 번만)
    app = Flask(__name__, 
               static_folder=static_folder,  # ← Frontend 빌드 결과물 경로
               static_url_path='')           # ← 루트 경로에서 서빙
    
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
    
    def add_spa_route(path, with_subpath=True):
        """SPA 라우트를 자동으로 추가하는 헬퍼 함수"""
        app.route(path)(serve_spa_routes)
        if with_subpath:
            app.route(f"{path}/<path:subpath>")(serve_spa_routes)
    
    # 헬스체크 엔드포인트 (범용 라우트보다 먼저 등록)
    @app.route('/api/health')
    def health_check():
        """컨테이너 헬스체크용 엔드포인트"""
        try:
            # 데이터베이스 연결 확인
            from database import get_db_connection
            db = get_db_connection()
            with db.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            db.close()
            
            return jsonify({
                "status": "healthy",
                "timestamp": time.time(),
                "service": "ywlab-backend",
                "version": DEPLOY_VERSION,
                "deploy_time": DEPLOY_TIMESTAMP
            }), 200
        except Exception as e:
            logger.error(f"헬스체크 실패: {str(e)}")
            return jsonify({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time(),
                "version": DEPLOY_VERSION
            }), 503
    
    # 배포 정보 확인용 엔드포인트 (간단한 확인용)
    @app.route('/api/deploy-info')
    def deploy_info():
        """배포 정보 확인용 엔드포인트"""
        return jsonify({
            "version": DEPLOY_VERSION,
            "deploy_time": DEPLOY_TIMESTAMP,
            "status": "deployed",
            "message": "배포 완료 확인됨"
        }), 200
    
    # Frontend 페이지 서빙 (추가)
    @app.route('/')
    def serve_frontend():
        """Frontend 메인 페이지 서빙"""
        try:
            logger.info(f"[DEBUG] serve_frontend 호출됨, static_folder: {app.static_folder}")
            logger.info(f"[DEBUG] index.html 존재 여부: {os.path.exists(os.path.join(app.static_folder, 'index.html'))}")
            return send_from_directory(app.static_folder, 'index.html')
        except FileNotFoundError:
            logger.error(f"[DEBUG] Frontend 빌드 파일을 찾을 수 없음: {app.static_folder}")
            return jsonify({"error": "Frontend 빌드 파일이 없습니다. 'npm run build'를 실행해주세요."}), 404
    
    # Vue Router SPA 라우팅 처리 (명시적 라우트)
    @app.route('/about')
    @app.route('/about/<path:subpath>')
    @app.route('/solutions')
    @app.route('/solutions/<path:subpath>')
    @app.route('/esg')
    @app.route('/esg/<path:subpath>')
    @app.route('/contact')
    @app.route('/login')
    @app.route('/admin')
    @app.route('/admin/<path:subpath>')
    def serve_spa_routes(subpath=None):
        """Vue Router SPA 라우팅 처리"""
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except FileNotFoundError:
            return jsonify({"error": "Frontend 빌드 파일이 없습니다."}), 404
    
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
        
        # 2. 메타데이터 파일 경로 확인
        metadata_path = os.path.join(os.path.dirname(__file__), 'metadata', 'docx', 'ywlabs_policy_20250609.docx')
        if not os.path.exists(metadata_path):
            logger.warning(f"[ChromaDB] 메타데이터 파일이 없습니다: {metadata_path}")
            logger.warning("[ChromaDB] RAG 컬렉션 초기화를 건너뜁니다.")
        else:
            logger.info(f"[ChromaDB] 메타데이터 파일 확인됨: {metadata_path}")
        
        # 3. 컬렉션 초기화 (DB -> RAG 순서)
        initialize_collections()
        logger.info("[ChromaDB] 모든 컬렉션 초기화 완료")
        
    except Exception as e:
        logger.error(f"[ChromaDB] 초기화 중 오류 발생: {str(e)}")
        # ChromaDB 초기화 실패 시에도 앱은 계속 실행
        logger.warning("[ChromaDB] 초기화 실패로 인해 벡터 검색 기능이 제한될 수 있습니다.")
    
    # 블루프린트 등록 (범용 라우트보다 먼저!)
    app.register_blueprint(chat_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(widget_bp)
    app.register_blueprint(legacy_bp)
    app.register_blueprint(auth_bp)

    # 범용 라우트 (블루프린트 등록 이후에 등록)
    @app.route('/<path:path>')
    def serve_static(path):
        """정적 파일 및 범용 SPA 라우팅 처리"""
        try:
            # API 경로는 백엔드에서 처리
            if path.startswith('api/'):
                return jsonify({"error": "API 엔드포인트를 찾을 수 없습니다."}), 404
            
            # 정적 파일이 존재하면 서빙
            file_path = os.path.join(app.static_folder, path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_from_directory(app.static_folder, path)
            
            # 2level 라우트 체크 (api가 아닌 첫 번째 레벨)
            path_parts = path.split('/')
            if len(path_parts) >= 1 and path_parts[0] and not path_parts[0].startswith('api'):
                # SPA 라우트로 처리 (index.html 반환)
                return send_from_directory(app.static_folder, 'index.html')
            
            # 파일이 없으면 404 반환
            return jsonify({"error": f"파일을 찾을 수 없습니다: {path}"}), 404
            
        except FileNotFoundError:
            # 파일이 없으면 404 반환
            return jsonify({"error": f"파일을 찾을 수 없습니다: {path}"}), 404

    # 환경 정보 스케줄러 시작
    environment_scheduler = start_scheduler()

    # 등록된 라우트 로깅
    logger.info("등록된 라우트:")
    for rule in app.url_map.iter_rules():
        logger.info(f"  {rule.endpoint}: {rule.rule}")

    return app

if __name__ == '__main__':
    # Flask 앱 생성
    app = create_app()
    
    # 배포 확인용 로그 (서버 시작 시 출력)
    logger = logging.getLogger(__name__)
    logger.info(f"✅ [DEPLOY] 서버 시작 완료 - 버전: {DEPLOY_VERSION}")
    logger.info(f"✅ [DEPLOY] 배포 시간: {DEPLOY_TIMESTAMP}")
    logger.info(f"Flask 서버 시작: http://0.0.0.0:8085 (환경: {get_config().profile})")
    
    app.run(host='0.0.0.0', port=8085, debug=get_config().DEBUG) 