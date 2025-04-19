from typing import List
from pyspark.sql import DataFrame


def calculate_on_time_flights(df: DataFrame) -> int:
    return df.filter((df["Cancelled"] == 0) & (df["Diverted"] == 0) & (df["ArrDelayMinutes"] == 0)).count()


def count_cancelled_flights(df: DataFrame) -> int:
    return df.filter(df["Cancelled"] != 0).count()


def count_diverted_flights(df: DataFrame) -> int:
    return df.filter(df["Diverted"] != 0).count()


def calculate_delayed_flights(df: DataFrame) -> int:
    return df.filter((df["Cancelled"] == 0) & (df["Diverted"] == 0) & (df["ArrDelayMinutes"] > 0)).count()


def monthly_flight_statistics(df: DataFrame) -> List:
    on_time_flight_count = calculate_on_time_flights(df)
    cancelled_flight_count = count_cancelled_flights(df)
    diverted_flight_count = count_diverted_flights(df)
    delayed_flight_count = calculate_delayed_flights(df)
    return [on_time_flight_count, cancelled_flight_count, diverted_flight_count, delayed_flight_count]
