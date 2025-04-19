from pyspark.sql import DataFrame
from pyspark.sql.functions import when, col, count


def causes_delay(df:DataFrame):
    cause_delay_df = df.select(
        count(when(col("CarrierDelay") != 0, 1)).alias("CarrierDelay"),
        count(when(col("WeatherDelay") != 0, 1)).alias("WeatherDelay"),
        count(when(col("NASDelay") != 0, 1)).alias("NASDelay"),
        count(when(col("SecurityDelay") != 0, 1)).alias("SecurityDelay"),
        count(when(col("LateAircraftDelay") != 0, 1)).alias("LateAircraftDelay")
    )
    return cause_delay_df.collect()[0].asDict()





