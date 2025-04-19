from hdfs import InsecureClient 
from logs.logger import logger
import os


def upload_to_hdfs(local_path, hdfs_path):
    hdfs_url = os.getenv('HDFS_URL', 'http://namenode:9870')
    hdfs_user = os.getenv('HDFS_USER', 'root')
    client = InsecureClient(hdfs_url, user=hdfs_user)
    client.upload(hdfs_path, local_path, overwrite=True)
    logger.info(f"Uploaded {local_path} to HDFS at {hdfs_path}")