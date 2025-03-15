import logging
import os
from datetime import datetime

logger = None

def get_logger():
    global logger
    if logger is None:
        setup_logger()
    return logger

def setup_logger():
    global logger
    if logger is None:
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", encoding='utf-8'),
                logging.StreamHandler()
            ],
            encoding='utf-8'
        )
        logger = logging.getLogger('migration')
    return logger