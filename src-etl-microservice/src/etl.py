from pyspark.sql import SparkSession

def etl_process(input_path, output_path):
    spark = SparkSession.builder \
        .appName("CSV to Parquet") \
        .getOrCreate()
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    df.write.parquet(output_path)
    spark.stop()