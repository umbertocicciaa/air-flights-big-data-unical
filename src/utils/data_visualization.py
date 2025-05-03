import os
from pyspark.sql import DataFrame, SparkSession

#hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")
#path =f"{hdfs_input_path}outputs"
path = "shared-filesystem/outputs"
delimiter = ","


def create_all_dataframe(spark: SparkSession):
    df = spark.read.options(delimiter=delimiter).parquet(path, header=True, inferSchema=True,
                                                         dateFormat='yyyy-MM-dd')
    return df


def create_month_dataframe(spark: SparkSession, month: int):
    df = spark.read.options(delimiter=delimiter).parquet(path, header=True, inferSchema=True,
                                                         dateFormat='yyyy-MM-dd')
    df = df.filter(df['Month'] == month)
    return df
