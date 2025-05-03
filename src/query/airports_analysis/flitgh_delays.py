from pyspark.sql import DataFrame
from pyspark.sql.functions import col, avg


def average_month_delay_for_city(df):
    avg_delay = df.dropna(subset=['ArrDelayMinutes']) \
        .filter(col('ArrDelayMinutes') > 0) \
        .agg(avg("ArrDelayMinutes")).collect()[0][0]

    avg_diverted = df.dropna(subset=['DivArrDelay']) \
        .agg(avg("DivArrDelay")).collect()[0][0]

    avg_delay = avg_delay if avg_delay is not None else 0
    avg_diverted = avg_diverted if avg_diverted is not None else 0

    return round((avg_delay + avg_diverted) / 2, 2)
