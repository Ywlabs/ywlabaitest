import logging
import os
from datetime import datetime

def setup_logger(name, log_file=None):
    """
    로거를 설정하고 반환합니다.
    
    Args:
        name (str): 로거 이름
        log_file (str, optional): 로그 파일 경로. 기본값은 None이며, 
                                 None인 경우 'logs/{name}_{date}.log' 형식으로 생성됩니다.
    
    Returns:
        logging.Logger: 설정된 로거 객체
    """
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 이미 핸들러가 있다면 추가하지 않음
    if logger.handlers:
        return logger
    
    # 로그 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 콘솔 핸들러 추가
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러 추가
    if log_file is None:
        # logs 디렉토리가 없으면 생성
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # 기본 로그 파일명 생성 (날짜 포함)
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = f'logs/{name}_{date_str}.log'
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger 