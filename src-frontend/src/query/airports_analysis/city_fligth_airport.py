from pyspark.sql import DataFrame


def city_flight_airport(df:DataFrame,city:str):
    df_city_airport_departure= df.filter((df["OriginCityName"]==city)).select("Origin").groupby("Origin").count()
    departure_fligth = {row['Origin']: row['count'] for row in df_city_airport_departure.collect()}

    df_city_airport_arrival= df.filter((df["DestCityName"]==city)).select("Dest").groupby("Dest").count()
    arrival_fligth = {row['Dest']: row['count'] for row in df_city_airport_arrival.collect()}

    both={}

    for city in set(departure_fligth.keys()).union(arrival_fligth.keys()):
        departure = departure_fligth.get(city, 0)
        arrival = arrival_fligth.get(city, 0)
        both[city] = [departure, arrival]

    return both

