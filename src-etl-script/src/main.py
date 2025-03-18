"""main.py"""
import json
from pyspark.sql import SparkSession

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, to_date
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def preprocess_data(df):
    df = df.dropna()
    logger.info("Dropped rows with null values")
    
    df = df.dropDuplicates()
    logger.info("Removed duplicate rows")
    
    df = df.withColumn("FlightDate", to_date(col("FlightDate"), "yyyy-MM-dd"))
    logger.info("Converted 'FlightDate' column to date type")
    
    string_columns = [field.name for field in df.schema.fields if field.dataType == 'StringType']
    for col_name in string_columns:
        df = df.withColumn(col_name, trim(col(col_name)))
    logger.info("Trimmed whitespace from string columns")
    
    df = df.filter(df["DepDelay"] >= 0)
    logger.info("Filtered out rows where 'DepDelay' is negative")
    
    df = df.fillna({'ArrDelay': 0})
    logger.info("Filled missing values in 'ArrDelay' with 0")
    
    df = df.withColumn("Speed", col("Distance") / col("AirTime"))
    logger.info("Created new column 'Speed' (Distance / AirTime)")
    
    df = df.withColumn("CRSDepTime", col("CRSDepTime").cast("string"))
    df = df.withColumn("CRSArrTime", col("CRSArrTime").cast("string"))
    logger.info("Converted 'CRSDepTime' and 'CRSArrTime' columns to string type")
    
    delay_columns = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    for col_name in delay_columns:
        df = df.fillna({col_name: 0})
    logger.info("Filled missing values in delay columns with 0")
    
    df = df.withColumn("TotalDelay", col("CarrierDelay") + col("WeatherDelay") + col("NASDelay") + col("SecurityDelay") + col("LateAircraftDelay"))
    logger.info("Created new column 'TotalDelay' (sum of all delay columns)")
    
    df = df.filter(df["Cancelled"] == 0)
    logger.info("Filtered out rows where 'Cancelled' is 1")
    
    columns_to_drop = [
        'CancellationCode', 'Diverted', 'DivAirportLandings', 'DivReachedDest', 'DivActualElapsedTime', 
        'DivArrDelay', 'DivDistance', 'Div1Airport', 'Div1AirportID', 'Div1AirportSeqID', 'Div1WheelsOn', 
        'Div1TotalGTime', 'Div1LongestGTime', 'Div1WheelsOff', 'Div1TailNum', 'Div2Airport', 'Div2AirportID', 
        'Div2AirportSeqID', 'Div2WheelsOn', 'Div2TotalGTime', 'Div2LongestGTime', 'Div2WheelsOff', 'Div2TailNum', 
        'Div3Airport', 'Div3AirportID', 'Div3AirportSeqID', 'Div3WheelsOn', 'Div3TotalGTime', 'Div3LongestGTime', 
        'Div3WheelsOff', 'Div3TailNum', 'Div4Airport', 'Div4AirportID', 'Div4AirportSeqID', 'Div4WheelsOn', 
        'Div4TotalGTime', 'Div4LongestGTime', 'Div4WheelsOff', 'Div4TailNum', 'Div5Airport', 'Div5AirportID', 
        'Div5AirportSeqID', 'Div5WheelsOn', 'Div5TotalGTime', 'Div5LongestGTime', 'Div5WheelsOff', 'Div5TailNum'
    ]
    df = df.drop(*columns_to_drop)
    logger.info("Dropped less useful columns for analysis")

    return df

def etl_process(input_path, output_path):
    logger.info(f"Starting ETL process for input: {input_path}, output: {output_path}")
    
    try:
        spark = SparkSession.builder \
            .appName("CSV to Parquet") \
            .getOrCreate()
        logger.info("Spark session created successfully")
        
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        logger.info(f"CSV file read successfully from {input_path}")
        
        df = preprocess_data(df)
        logger.info("Data preprocessing completed")

        df.write.parquet(output_path)
        logger.info(f"Data written to Parquet format at {output_path}")
        
    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise
    finally:
        spark.stop()
        logger.info("Spark session stopped")

def read_parquet(parquet_path):
    spark = SparkSession.builder \
        .appName("ReadParquet") \
        .getOrCreate()

    data = spark.read.parquet(parquet_path)
    data.show()

    spark.stop()

if __name__ == "__main__":
    input_path = "/mnt/shared-filesystem/inputs/"
    output_path = "/mnt/shared-filesystem/outputs/"
    etl_process(input_path, output_path)
    read_parquet(output_path)