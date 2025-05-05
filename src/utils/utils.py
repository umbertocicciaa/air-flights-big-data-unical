import locale
import os
import airportsdata
import pandas as pd
from datetime import datetime, timedelta


def number_from_month(month):
    months = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12
    }
    return months.get(month.lower(), "month not valid")

def month_from_number(number):
    months = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    return months.get(number, "number not valid")


def get_cities():
    file_path = os.path.join(os.path.dirname(__file__), 'airports.txt')
    with open(file_path, 'r') as file:
        cities = list(eval(file.read()))
    return cities


def get_sorted_city_list():
    return sorted(get_cities())


def get_coordinates_city(address):
    df = dataframe_from_cities_coordinates()
    if address in df.index:
        coords = df.loc[address]
        return [coords['lat'], coords['lon']]
    else:
        return None


def get_airport_coordinates(code) -> dict:
    airports = airportsdata.load("IATA")
    airport = airports.get(code.upper())
    if airport:
        return {
            "name": airport["name"],
            "lat": airport["lat"],
            "lon": airport["lon"]
        }
    else:
        return None


def dataframe_from_cities_coordinates():
    file_path = os.path.join(os.path.dirname(__file__), 'city_lat_long.csv')
    df = pd.read_csv(file_path)
    df.set_index("citta", inplace=True)
    return df


def get_city_coordinate():
    df = dataframe_from_cities_coordinates()
    dict = df.to_dict(orient='index')
    for city, coords in dict.items():
        dict[city] = [coords['lat'], coords['lon']]
    return dict
