import logger
from .session_spark import create_session
import os

log_path = os.getenv("LOG_PATH", "/mnt/shared-filesystem/logs")
file_path = os.getenv("HDFS_INPUT_PATH", "/outputs")

os.makedirs(log_path, exist_ok=True)


def read_parquet(parquet_path):
    spark = create_session() 
    data = spark.read.parquet(parquet_path)
    spark.stop()
    return data

def load_parquet_data():
    try:
        logger.info("Loading data from Parquet file")
        data_pd = read_parquet(file_path) 
        logger.info("Data loaded from Parquet file and cached in Redis")
        return data_pd
    
    except Exception as e:
        logger.error(f"Error loading Parquet file: {e}")
        return None