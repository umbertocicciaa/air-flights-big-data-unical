"""main.py"""
from pyspark.sql import SparkSession
import logging
import os
from hdfs import InsecureClient

os.makedirs("/mnt/shared-filesystem/logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/shared-filesystem/logs/etl_script_process.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def convert_minutes_to_hhmm(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{int(hours):02d}:{int(mins):02d}"

def preprocess_data(df):
    selecte_columns = ["Year","Quarter","Month","DayofMonth","DayOfWeek","FlightDate","Reporting_Airline","Tail_Number","Flight_Number_Reporting_Airline", "OriginAirportID","Origin","OriginCityName","OriginStateName","DestAirportID" ,"Dest","DestCityName","DestStateName","CRSDepTime","DepTime","DepDelay","CRSArrTime" ,"ArrTime","ArrDelay","Cancelled","CRSElapsedTime","ActualElapsedTime" ,"AirTime","Flights","Distance"]
    df_processed = df.select(*selecte_columns)
    time_columns = ["CRSDepTime", "DepTime", "CRSArrTime", "ArrTime"]
    
    for col_name in time_columns:
        df_processed = df_processed.withColumn(col_name, 
            df_processed[col_name].substr(1, 2).cast("string").concat(":").concat(df_processed[col_name].substr(3, 2).cast("string"))
        )
    df_processed = df_processed.withColumn("Cancelled", 
        df_processed["Cancelled"].cast("string").replace({"0": "not cancelled", "1": "cancelled"})
    )

    time_columns_in_minutes = ["AirTime", "CRSElapsedTime", "ActualElapsedTime"]
    
    for col_name in time_columns_in_minutes:
        df_processed = df_processed.withColumn(col_name, 
            convert_minutes_to_hhmm(df_processed[col_name].cast("int"))
        )
    return df_processed

def upload_to_hdfs(local_path, hdfs_path):
    client = InsecureClient('http://hadoop-namenode:9870', user='hdfs')
    client.upload(hdfs_path, local_path, overwrite=True)
    logger.info(f"Uploaded {local_path} to HDFS at {hdfs_path}")

def etl_process(input_path, output_path):
    logger.info(f"Starting ETL process for input: {input_path}, output: {output_path}")
    
    try:
        spark = SparkSession.builder \
            .master("spark://spark:7077") \
            .appName("CSV to Parquet") \
            .getOrCreate()
        logger.info("Spark session created successfully")
        
        df = spark.read.csv(input_path, header=True)
        logger.info(f"CSV file read successfully from {input_path}")
        
        df_processed = preprocess_data(df)
        logger.info("Data preprocessing completed")

        df_processed.write.mode("overwrite").parquet(output_path)
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

    logger.info(f"Data: {data.collect()}")
    logger.info(f"Data schema: {data.schema}")
    logger.info(f"Total records: {data.count()}")

    spark.stop()

if __name__ == "__main__":
    local_input_path = "/mnt/shared-filesystem/inputs/"
    hdfs_input_path = "/inputs"
    local_output_path = "/mnt/shared-filesystem/outputs/"
    hdfs_output_path = "/outputs"

    upload_to_hdfs(local_input_path, hdfs_input_path)

    etl_process(hdfs_input_path, hdfs_output_path)
    
    read_parquet(hdfs_output_path)