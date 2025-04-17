import os
from services.etl import etl_process
from services.hadoopfs import upload_to_hdfs
from services.datasets import read_parquet
from dotenv import load_dotenv
load_dotenv()

os.makedirs(os.getenv("LOGS_PATH", "/mnt/shared-filesystem/logs"), exist_ok=True)
local_input_path = os.getenv("LOCAL_INPUT_PATH", "/mnt/shared-filesystem/inputs/")
hdfs_input_path = os.getenv("HDFS_INPUT_PATH", "/inputs")
local_output_path = os.getenv("LOCAL_OUTPUT_PATH", "/mnt/shared-filesystem/outputs/")
hdfs_output_path = os.getenv("HDFS_OUTPUT_PATH", "/outputs")

if __name__ == "__main__":
    upload_to_hdfs(local_input_path, hdfs_input_path)
    etl_process(hdfs_input_path, hdfs_output_path)
    dataset = read_parquet(hdfs_output_path)