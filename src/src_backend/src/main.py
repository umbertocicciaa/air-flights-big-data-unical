import os
from utils.hadoopfs import upload_to_hdfs
from utils.datasets import read_parquet
from dotenv import load_dotenv

load_dotenv(dotenv_path="src_backend/local.env")

os.makedirs(os.getenv("LOGS_PATH", "shared-filesystem/logs"), exist_ok=True)
local_input_path = os.getenv("LOCAL_INPUT_PATH", "shared-filesystem/inputs/")
hdfs_input_path = os.getenv("HDFS_INPUT_PATH", "/inputs")
local_output_path = os.getenv("LOCAL_OUTPUT_PATH", "shared-filesystem/outputs/")
hdfs_output_path = os.getenv("HDFS_OUTPUT_PATH", "/outputs")

if __name__ == "__main__":
    # upload_to_hdfs(local_input_path, hdfs_input_path)
    # etl_process(hdfs_input_path, hdfs_output_path)
    upload_to_hdfs(local_output_path, hdfs_output_path)
    dataset = read_parquet(hdfs_output_path)
