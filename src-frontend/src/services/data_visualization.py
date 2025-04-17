import os
from pyspark.sql import DataFrame, SparkSession

local_input_path = os.getenv("LOCAL_INPUT_PATH", "/mnt/shared-filesystem/inputs/")
hdfs_input_path = os.getenv("HDFS_INPUT_PATH", "/inputs")
local_output_path = os.getenv("LOCAL_OUTPUT_PATH", "/mnt/shared-filesystem/outputs/")
hdfs_output_path = os.getenv("HDFS_OUTPUT_PATH", "air-flights-big-data-unical/shared-filesystem/outputs")
delimiter = ","

def create_all_dataframe (spark:SparkSession) -> DataFrame:
    df = None
    df = spark.read.options(delimiter=delimiter).parquet(hdfs_output_path, header=True, inferSchema=True, dateFormat='yyyy-MM-dd')
    return df

def create_month_dataframe(spark:SparkSession, month:int)-> DataFrame:

    df = spark.read.options(delimiter=delimiter).parquet(hdfs_output_path[month-1], header=True, inferSchema=True,
                                                     dateFormat='yyyy-MM-dd')
    return df