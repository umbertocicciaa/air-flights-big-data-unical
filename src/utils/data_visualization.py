import os
from utils.datasets import read_parquet

#hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")
#path =f"{hdfs_input_path}outputs"
#path = "shared-filesystem/outputs"
hdfs_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000")
hdfs_output_path = os.getenv("HDFS_OUTPUT_PATH", "/outputs")
output_path = hdfs_path + hdfs_output_path.lstrip("/")
path = output_path

def create_all_dataframe():
    return read_parquet(path)

def create_month_dataframe(month: int):
    df = read_parquet(path)
    month_string = str((month+1))
    df = df.filter(df['Month'] == month_string)
    return df
