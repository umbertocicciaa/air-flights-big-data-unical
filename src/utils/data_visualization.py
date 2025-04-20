import os
from pyspark.sql import DataFrame, SparkSession

hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")
path =f"{hdfs_input_path}outputs"
delimiter = ","


def create_all_dataframe(spark: SparkSession) -> DataFrame:
    df = spark.read.options(delimiter=delimiter).parquet(path, header=True, inferSchema=True,
                                                         dateFormat='yyyy-MM-dd')
    return df


def create_month_dataframe(spark: SparkSession, month: int) -> DataFrame:
    df = spark.read.options(delimiter=delimiter).parquet(path[month - 1], header=True, inferSchema=True,
                                                         dateFormat='yyyy-MM-dd')
    return df
