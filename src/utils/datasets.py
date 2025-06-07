import re

import pandas as pd
from utils.session_spark import create_session
from logs.logger import logger

def read_parquet(parquet_path):
    logger.info(f"Reading parquet file from {parquet_path}")
    spark = create_session()
    data = spark.read.parquet(f"{parquet_path}/*")
    return data