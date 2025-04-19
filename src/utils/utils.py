import locale
import os
import airportsdata
import pandas as pd
from geopy import Nominatim
from datetime import datetime, timedelta


def month_from_number(number):
    months = {
        1: "january", 2: "february", 3: "march", 4: "april",
        5: "may", 6: "june", 7: "july", 8: "august",
        9: "september", 10: "october", 11: "november", 12: "december"
    }
    return months.get(number, "number not valid")

def previous_month(month):
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
    today = datetime.strptime(f"01 {month} 2023", "%d %B %Y")
    previous_date = today - timedelta(days=1)
    return previous_date.strftime("%B")


def get_cities():
    file_path = os.path.join(os.path.dirname(__file__), 'airports.txt')
    with open(file_path, 'r') as file:
        cities = list(eval(file.read()))
    return cities


def get_sorted_city_list():
    return sorted(get_cities())


def get_coordinates_city(address):
    geolocator = Nominatim(user_agent="myGeocoderApp")
    location = geolocator.geocode(address, timeout=10)
    if location:
        return [location.latitude, location.longitude]
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
