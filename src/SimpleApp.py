"""SimpleApp.py"""
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master('spark://127.0.0.1:7077') \
    .appName("SimpleApp") \
    .getOrCreate()

spark.stop()