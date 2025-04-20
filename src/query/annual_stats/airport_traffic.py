import pandas as pd
from pandas import DataFrame
from query.airports_analysis.fligth_numbers import calculate_departure_arrival_counts
from utils.utils import get_coordinates_city


def most_traffic_city(df: DataFrame) -> DataFrame:
    city = ["Atlanta, GA", "Dallas/Fort Worth, TX", "Denver, CO", "Chicago, IL", "Charlotte, NC","Orlando, FL", "Las Vegas, NV", "Phoenix, AZ", "New York, NY", "Seattle, WA"]

    results = []
    for city_name in city:
        coor = get_coordinates_city(city_name)
        if coor is not None:
            latitudine = coor[0]
            longitudine = coor[1]
            val1, val2 = calculate_departure_arrival_counts(df, city_name)
            num = val1 + val2
            results.append({"city": city_name, "lat": latitudine, "lon": longitudine, "num": num})
    return pd.DataFrame(results)
