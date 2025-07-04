from pyspark.sql import DataFrame
from pyspark.sql.functions import column, count


def destinations_number_city(df:DataFrame, city:str):
    city= df.filter(df["OriginCityName"] == city)
    city_dest_fligths=city.groupby(df["DestCityName"]).agg(count(("*")).alias("NumberFlights")).orderBy(column("NumberFlights").desc())
    top_airports = city_dest_fligths.collect()
    return {row["DestCityName"]: row["NumberFlights"] for row in top_airports}
