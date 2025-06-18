import os
from pyspark import SparkConf
from pyspark.sql import SparkSession

def create_session():
    spark_master = os.getenv('SPARK_MASTER', 'spark://spark-master:7077')
    
    app_name = os.getenv('SPARK_APP_NAME', 'Spark Context')
    conf = SparkConf()
    
    conf.set("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000")
    conf.set("spark.hadoop.dfs.client.use.datanode.hostname", "false")
    conf.set("spark.hadoop.dfs.datanode.use.datanode.hostname", "false")
    conf.set("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem")
    conf.set("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    
    conf.set("spark.hadoop.security.authentication", "simple")
    conf.set("spark.hadoop.security.authorization", "false")
    
    conf.set("spark.driver.memory", "8g")
    conf.set("spark.executor.memory", "6g")
    
    spark = (SparkSession.builder
             .appName(app_name)
             .master(spark_master)
             .config(conf=conf)
             .getOrCreate())
    
    return spark
