from pyspark.sql import SparkSession
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def etl_process(input_path, output_path):
    logger.info(f"Starting ETL process for input: {input_path}, output: {output_path}")
    
    try:
        spark = SparkSession.builder \
            .appName("CSV to Parquet") \
            .getOrCreate()
        logger.info("Spark session created successfully")
        
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        logger.info(f"CSV file read successfully from {input_path}")
        
        df.write.parquet(output_path)
        logger.info(f"Data written to Parquet format at {output_path}")
        
    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise
    finally:
        spark.stop()
        logger.info("Spark session stopped")