from logs.logger import logger
from utils.session_spark import create_session


def read_parquet(parquet_path):
    spark = create_session()

    data = spark.read.parquet(parquet_path)

    logger.info(f"Data: {data.collect()}")
    logger.info(f"Data schema: {data.schema}")
    logger.info(f"Total records: {data.count()}")

    return data
