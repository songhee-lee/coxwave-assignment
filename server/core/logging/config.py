import logging
import os
from dotenv import load_dotenv
load_dotenv()

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "debug.log")

def setup_logging(name):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),  # 로그를 파일로 저장
            logging.StreamHandler()              # 표준 출력에도 로그 출력
        ]
    )
    logger = logging.getLogger(name)
    return logger