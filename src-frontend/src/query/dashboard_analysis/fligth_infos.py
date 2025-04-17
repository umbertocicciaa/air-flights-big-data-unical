from typing import List
from pyspark.sql import DataFrame


def calculateOnTimeFlights(df: DataFrame)-> int:
    return df.filter((df["Cancelled"] == 0) & (df["Diverted"] == 0) & (df["ArrDelayMinutes"] == 0)).count()

def countCancelledFlights(df: DataFrame)-> int:
    return df.filter(df["Cancelled"] != 0).count()

def countDivertedFlights(df: DataFrame)-> int:
    return df.filter(df["Diverted"] != 0).count()

def calculateDelayedFlights(df: DataFrame)->int:
    return df.filter((df["Cancelled"] == 0) & (df["Diverted"] == 0) & (df["ArrDelayMinutes"] > 0)).count()

def monthly_flight_statistics(df: DataFrame) -> List:
    on_time_flight_count = calculateOnTimeFlights(df)
    cancelled_flight_count = countCancelledFlights(df)
    diverted_flight_count = countDivertedFlights(df)
    delayed_flight_count = calculateDelayedFlights(df)
    return [on_time_flight_count,cancelled_flight_count,diverted_flight_count,delayed_flight_count]

