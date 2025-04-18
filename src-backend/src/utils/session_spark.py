import os
from pyspark.sql import SparkSession
from pyspark import SparkConf

def create_session():
    hdfs_url = os.getenv('HDFS_URL', 'hdfs://localhost:9000')
    spark_master = os.getenv('SPARK_MASTER', 'spark://localhost:7077')
    
    app_name = os.getenv('SPARK_APP_NAME', 'CSV to Parquet')
    conf = SparkConf()
    conf.set("spark.hadoop.fs.defaultFS", hdfs_url)

    spark = SparkSession.builder \
        .master(spark_master) \
        .config(conf=conf) \
        .appName(app_name) \
        .getOrCreate()
    return spark