import os
from pyspark.sql import SparkSession
from pyspark import SparkConf

def create_session():
    hdfs_url = os.getenv('HDFS_URL', 'http://hadoop-namenode:9870')
    spark_master = os.getenv('SPARK_MASTER', 'spark://spark:7077')
    
    app_name = os.getenv('SPARK_APP_NAME', 'CSV to Parquet')
    conf = SparkConf()
    conf.set("spark.hadoop.fs.defaultFS", hdfs_url)
    conf.set("dfs.client.rpc.max-response-size", os.getenv('DFS_CLIENT_RPC_MAX_RESPONSE_SIZE', "5368709120"))
    conf.set("dfs.datanode.max.transfer.threads", os.getenv('DFS_DATANODE_MAX_TRANSFER_THREADS', "4096"))

    spark = SparkSession.builder \
        .master(spark_master) \
        .config(conf=conf) \
        .appName(app_name) \
        .getOrCreate()
    return spark