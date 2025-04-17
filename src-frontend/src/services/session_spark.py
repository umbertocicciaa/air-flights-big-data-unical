import os
from pyspark.sql import SparkSession
from pyspark import SparkConf
from dotenv import load_dotenv
load_dotenv(dotenv_path='src-frontend/local.env')

def create_session():
    hdfs_url = os.getenv('HDFS_URL', 'http://localhost:9870')
    spark_master = os.getenv('SPARK_MASTER', 'spark://localhost:7077')
    
    app_name = os.getenv('SPARK_APP_NAME', 'Frontend')
    conf = SparkConf()
    conf.set("spark.hadoop.fs.defaultFS", hdfs_url)
    
    print(spark_master)

    spark = SparkSession.builder.master(spark_master).config(conf=conf).appName(app_name).getOrCreate()
    return spark