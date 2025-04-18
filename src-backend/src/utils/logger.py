import logging
import os
from dotenv import load_dotenv
load_dotenv()

log_level = os.getenv('LOG_LEVEL', 'INFO')
log_file_path = os.getenv('LOG_FILE_PATH', 'shared-filesystem/logs/etl_script_process.log')

logging.basicConfig(
    level=getattr(logging, log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
