from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def average(df: DataFrame):
    not_diverted = df.filter(col('Diverted') == 0)
    diverted = df.filter(col('Diverted') != 0)

    avg = {}

    avg['average_delay_direct'] = df.dropna(subset=['ArrDelayMinutes']) \
        .filter(col('ArrDelayMinutes') > 0) \
        .agg(avg("ArrDelayMinutes")).collect()[0][0]

    avg['average_delay_diverted'] = df.dropna(subset=['DivArrDelay']) \
        .agg(avg("DivArrDelay")).collect()[0][0]

    avg['average_distance_direct'] = not_diverted.agg(avg("Distance")).collect()[0][0]
    avg['average_distance_diverted'] = diverted.agg(avg("DivDistance")).collect()[0][0]

    avg['average_flight_minutes_direct'] = df.agg(avg("ActualElapsedTime")).collect()[0][0]
    avg['average_flight_minutes_diverted'] = df.agg(avg("DivActualElapsedTime")).collect()[0][0]

    return avg


def calculate_monthly_flight_statistics(df: DataFrame):
    total_fligths = df.count()
    avg = average(df)
    avg_delay = round((avg['average_delay_direct'] + avg['average_delay_diverted']) / 2, 2)
    avg_distance = round((avg['average_distance_direct'] + avg['average_distance_diverted']) / 2, 2)
    average_flight_duration = round(
        (avg['average_flight_minutes_direct'] + avg['average_flight_minutes_diverted']) / 2, 2)

    return [total_fligths, avg_delay, avg_distance, average_flight_duration]
