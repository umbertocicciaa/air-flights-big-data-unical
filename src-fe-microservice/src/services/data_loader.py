import pickle
import pandas as pd
from .redis_connection import init_redis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

file_path = "/mnt/shared-filesystem/outputs/"
redis_key = "parquet_data"


def read_parquet(parquet_path):
    logger.info(f"Reading Parquet file from path: {parquet_path}")
    data = pd.read_parquet(parquet_path)
    logger.info("Successfully read Parquet file")
    return data

def load_parquet_data():
    redis_cli = init_redis()
    cached_data = redis_cli.get(redis_key)
    
    if cached_data:
        try:
            logger.info("Loading data from Redis cache")
            data = pickle.loads(cached_data)
            return data
        except Exception as e:
            logger.error(f"Error loading data from Redis: {e}")

    try:
        logger.info("Loading data from Parquet file")
        data_pd = read_parquet(file_path) 
        serialized_df = pickle.dumps(data_pd)
        redis_cli.set(redis_key, serialized_df)
        logger.info("Data loaded from Parquet file and cached in Redis")
        return data_pd
    
    except Exception as e:
        logger.error(f"Error loading Parquet file: {e}")
        return None