from apscheduler.schedulers.background import BackgroundScheduler
from services.vector_service import validate_vector_store
from common.logger import setup_logger

logger = setup_logger('vector_scheduler')

def update_vector_store_job():
    """벡터 스토어 검증 작업"""
    try:
        logger.info("벡터 스토어 검증 시작")
        validate_vector_store()
        logger.info("벡터 스토어 검증 완료")
    except Exception as e:
        logger.error(f"벡터 스토어 검증 실패: {str(e)}")

def start_scheduler():
    """스케줄러 시작"""
    scheduler = BackgroundScheduler()
    
    # 매일 새벽 3시에 벡터 스토어 검증 작업 실행
    scheduler.add_job(
        update_vector_store_job,
        'cron',
        hour=3,
        id='update_vector_store',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("벡터 스토어 스케줄러 시작됨")
    
    return scheduler 