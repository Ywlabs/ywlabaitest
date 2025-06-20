from apscheduler.schedulers.background import BackgroundScheduler
from services.environment_service import environment_service
from common.logger import setup_logger

logger = setup_logger('environment_scheduler')

def update_environment_job():
    """환경 정보 업데이트 작업"""
    try:
        logger.info("환경 정보 업데이트 시작")
        environment_service.update_environment_data()
        logger.info("환경 정보 업데이트 완료")
    except Exception as e:
        logger.error(f"환경 정보 업데이트 실패: {str(e)}")

def start_scheduler():
    """스케줄러 시작"""
    scheduler = BackgroundScheduler()
    
    # 10분마다 환경 정보 업데이트
    scheduler.add_job(
        update_environment_job,
        'interval',
        minutes=100,
        id='update_environment',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("환경 정보 스케줄러 시작됨")
    
    return scheduler 