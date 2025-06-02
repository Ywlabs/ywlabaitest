from apscheduler.schedulers.background import BackgroundScheduler
from services.vector_service import validate_vector_store

def init_scheduler():
    """스케줄러 초기화 및 작업 등록"""
    scheduler = BackgroundScheduler()
    
    # 매일 새벽 3시에 벡터 스토어 검증 작업 실행
    scheduler.add_job(
        validate_vector_store,
        'cron',
        hour=3,
        id='vector_store_validation'
    )
    
    # 스케줄러 시작
    scheduler.start()
    
    return scheduler 