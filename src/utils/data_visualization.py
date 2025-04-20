import os
from pyspark.sql import DataFrame, SparkSession

hdfs_input_path = os.getenv("HDFS_INPUT_PATH", "hdfs://namenode:9000/outputs/")
delimiter = ","


def create_all_dataframe(spark: SparkSession) -> DataFrame:
    df = spark.read.options(delimiter=delimiter).parquet(hdfs_input_path, header=True, inferSchema=True,
                                                         dateFormat='yyyy-MM-dd')
    return df


def create_month_dataframe(spark: SparkSession, month: int) -> DataFrame:
    df = spark.read.options(delimiter=delimiter).parquet(hdfs_input_path[month - 1], header=True, inferSchema=True,
                                                         dateFormat='yyyy-MM-dd')
    return df
