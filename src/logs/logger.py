import logging
import os


log_level = os.getenv('LOG_LEVEL', 'INFO')
log_file_path = os.getenv('LOG_FILE_PATH', '~/mnt/shared-filesystem/logs/')

logging.basicConfig(
    level=getattr(logging, log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path+'etl_script_process.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
