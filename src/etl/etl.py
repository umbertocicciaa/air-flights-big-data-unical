from preprocesing import preprocess_data
from ..utils.session_spark import create_session
from ..logs.logger import logger


def etl_process(input_path, output_path):
    logger.info(f"Starting ETL process for input: {input_path}, output: {output_path}")

    try:
        spark = create_session()

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
