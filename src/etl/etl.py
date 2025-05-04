import os
from etl.preprocesing import preprocess_data
from utils.session_spark import create_session
from logs.logger import logger


#hdfs_path = os.getenv("HDFS_PATH", "hdfs://localhost:9000/")
path="shared-filesystem/"
def etl_process(input_path : str, output_path : str):
    #input_path = hdfs_path + (input_path.lstrip("/"))
    #output_path = hdfs_path + (output_path.lstrip("/"))
    input_path = path + (input_path.lstrip("/"))
    output_path = path + (output_path.lstrip("/"))
    logger.info(f"Starting ETL process for input: {input_path}, output: {output_path}")

    try:
        spark = create_session()

        input_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.csv')]    
        df = None
    
        for csv_file in input_files:
            delimiter = ","
            if df is None:
                df = spark.read.options(delimiter=delimiter).csv(csv_file, header=True, inferSchema=True, dateFormat='yyyy-MM-dd')
            else:
                df = df.union(spark.read.options(delimiter=delimiter).csv(csv_file, header=True, inferSchema=True, dateFormat='yyyy-MM-dd'))
        logger.info(f"CSV file read successfully from {input_path}")
          
        df_processed = preprocess_data(df)
        logger.info("Data preprocessing completed")

        df_processed.write.mode("overwrite").parquet(output_path)
        logger.info(f"Data written to Parquet format at {output_path}")

    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise e
    else:
        spark.stop()
        logger.info("ETL process completed successfully")
        logger.info("Spark session stopped")
