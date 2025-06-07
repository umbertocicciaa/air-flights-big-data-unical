from pyspark.sql import DataFrame
from pyspark.sql.functions import to_timestamp, lpad, col


def preprocess_data(df : DataFrame):
    df = df.withColumn("CRSDepTime", to_timestamp(lpad(col("CRSDepTime").cast("string"), 4, "0"), "HHmm"))
    df = df.withColumn("DepTime", to_timestamp(lpad(col("DepTime").cast("string"), 4, "0"), "HHmm"))
    df = df.withColumn("CRSArrTime", to_timestamp(lpad(col("CRSArrTime").cast("string"), 4, "0"), "HHmm"))
    df = df.withColumn("ArrTime", to_timestamp(lpad(col("ArrTime").cast("string"), 4, "0"), "HHmm"))
    return df
