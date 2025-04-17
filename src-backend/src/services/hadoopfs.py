from hdfs import InsecureClient 
from utils.logger import logger
import os
from dotenv import load_dotenv
load_dotenv()

def upload_to_hdfs(local_path, hdfs_path):
    hdfs_url = os.getenv('HDFS_URL', 'http://hadoop-namenode:9870')
    hdfs_user = os.getenv('HDFS_USER', 'superuser')
    client = InsecureClient(hdfs_url, user=hdfs_user)
    client.upload(hdfs_path, local_path, overwrite=True)
    logger.info(f"Uploaded {local_path} to HDFS at {hdfs_path}")