import datetime
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, to_timestamp


def get_flight(df: DataFrame, data: datetime.date, origine: str, destinazione: str, ora: datetime.time) -> DataFrame:
    ora_ts = to_timestamp(lit(ora.strftime("%H:%M")), "HH:mm")
    voliFiltrati = df.filter(df["FlightDate"] == data).filter(df["OriginCityName"] == origine).filter(
        df["DestCityName"] == destinazione).filter(df["CRSDepTime"] == ora_ts)
    return voliFiltrati.select("Origin", "Dest", "Distance", "Flight_Number_Reporting_Airline", "CRSDepTime", "DepTime",
                               "DepDelay", "CRSArrTime", "ArrTime", "ArrDelay",
                               "ArrDelayMinutes", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay",
                               "LateAircraftDelay",
                               "Cancelled", "Diverted", "DivReachedDest", "Div1Airport", "Div2Airport", "Div3Airport",
                               "Div4Airport", "Div5Airport")


def get_flight_advanced_delay(df: DataFrame) -> DataFrame:
    return df.filter(df["ArrDelayMinutes"] <= 0)


def get_flight_advanced_canc(df: DataFrame) -> DataFrame:
    return df.filter(df["Cancelled"] == 0)


def get_flight_advanced_div(df: DataFrame) -> DataFrame:
    return df.filter(df["Diverted"] == 0)
