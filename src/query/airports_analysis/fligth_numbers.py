from pyspark.sql import DataFrame


def calculate_departure_arrival_counts(df: DataFrame, city: str):
    counts = df.filter((df["OriginCityName"] == city) | (df["DestCityName"] == city)) \
        .groupBy(
        (df["OriginCityName"] == city).alias("is_departure"),
        (df["DestCityName"] == city).alias("is_arrival")
    ).count()

    departures = counts.filter(counts["is_departure"] == True).agg({"count": "sum"}).collect()[0][0] or 0
    arrivals = counts.filter(counts["is_arrival"] == True).agg({"count": "sum"}).collect()[0][0] or 0

    return departures, arrivals
