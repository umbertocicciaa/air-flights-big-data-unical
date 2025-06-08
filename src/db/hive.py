from pyhive import hive, presto
from pyspark.sql import SparkSession
import pandas as pd

class HivePrestoClient:
    def __init__(
        self,
        hive_host="hive-server",
        hive_port=10000,
        hive_username="hive",
        presto_host="presto-coordinator",
        presto_port=8089,
        presto_catalog="hive",
        presto_schema="default"
    ):
        self.hive_conn = hive.Connection(
            host=hive_host,
            port=hive_port,
            username=hive_username,
            database="default"
        )
        self.presto_conn = presto.connect(
            host=presto_host,
            port=presto_port,
            catalog=presto_catalog,
            schema=presto_schema
        )

    def ensure_database(self, db_name):
        with self.hive_conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    def save_dataframe_as_table(self, df, db_name, table_name, mode="overwrite"):
        self.ensure_database(db_name)
        df.write.saveAsTable(f"{db_name}.{table_name}", mode=mode)

    def presto_query(self, query):
        return pd.read_sql(query, self.presto_conn)

# Example usage:
# client = HivePrestoClient()
# spark_df = client.spark.createDataFrame([("foo", 1), ("bar", 2)], ["name", "value"])
# client.save_dataframe_as_table(spark_df, "testdb", "mytable")
# result_df = client.presto_query("SELECT * FROM testdb.mytable")
# print(result_df)