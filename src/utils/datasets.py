from utils.session_spark import create_session


def read_parquet(parquet_path):
    spark = create_session()
    data = spark.read.parquet(parquet_path)
    if not data.is_cached:
        data.cache()
    return data
