import os

from etl.preprocesing import preprocess_data
from logs.logger import logger
from utils.session_spark import create_session

def etl_process(input_path: str, output_path: str):
    hdfs_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000")
    input_path = hdfs_path + input_path.lstrip("/")
    output_path = hdfs_path + output_path.lstrip("/")
    
    logger.info(f"Starting ETL process for input: {input_path}, output: {output_path}")
    spark = None
    try:
        spark = create_session()
        
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)
        logger.info(f"CSV files read successfully from {input_path}")
        logger.info(f"Colonne lette: \n {df.columns} \n Prime cinque righe: {df.head(5)} \n")

        df_processed = preprocess_data(df)
        logger.info("Data preprocessing completed")
        logger.info(f"Colonne preprocessed: \n {df_processed.columns} \n Prime cinque righe: {df_processed.head(5)} \n")
        
        df_processed.write.mode("overwrite").parquet(output_path)
        logger.info(f"Data written to Parquet format at {output_path}")
        logger.info("ETL process completed successfully")
    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise e
    finally:
        logger.info("ETL process completed successfully")
        logger.info("Spark session stopped")
        if spark:
            spark.stop()