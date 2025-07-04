import datetime

from pyspark.sql import DataFrame
from logs.logger import logger

def get_flight(df: DataFrame, data: datetime.date, origine: str, destinazione: str) -> DataFrame:
    data_str = data.strftime("%Y-%m-%d")
    logger.info(f"Data {data_str}, per il volo da {origine} a {destinazione}")
    voliFiltrati = df.filter(df["FlightDate"] == data_str) \
        .filter(df["OriginCityName"] == origine) \
        .filter(df["DestCityName"] == destinazione)

    return voliFiltrati.select("Origin", "Dest", "Distance", "Flight_Number_Reporting_Airline", "CRSDepTime",
                               "DepTime", "DepDelay", "CRSArrTime", "ArrTime", "ArrDelay", "ArrDelayMinutes",
                               "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay",
                               "Cancelled", "Diverted", "DivReachedDest", "Div1Airport", "Div2Airport", "Div3Airport",
                               "Div4Airport", "Div5Airport")


def get_flight_advanced_delay(df: DataFrame):
    return df.filter(df["ArrDelayMinutes"] <= 0)


def get_flight_advanced_canc(df: DataFrame):
    return df.filter(df["Cancelled"] == 0)


def get_flight_advanced_div(df: DataFrame):
    return df.filter(df["Diverted"] == 0)
