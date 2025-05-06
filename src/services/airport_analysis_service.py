import pandas as pd

from utils.utils import get_city_coordinate, get_airport_coordinates

def create_dataframe_pandas_to_visualize_delays(delay_list):
    df = pd.DataFrame({'ritardi partenze': delay_list[0], 'ritardi arrivi': delay_list[1]})
    df.index = range(1, 13)
    return df

def create_dataframe_pandas_to_visualize_city_coordinates(lista_citta):
    cities = []
    latitudine = []
    longitudine = []
    dict_citta_coordinate = get_city_coordinate()
    for citta in lista_citta:
        if citta in dict_citta_coordinate:
            coordinates = dict_citta_coordinate[citta]
            cities.append(citta)
            latitudine.append(coordinates[0])
            longitudine.append(coordinates[1])
    return pd.DataFrame({"name": cities, 'lat': latitudine, 'lon': longitudine})

def create_dataframe_pandas_to_visualize_map_airports_coordinates(aeroporti):
    airport_name = []
    airport_lat = []
    airport_lon = []

    for aeroporto in aeroporti:
        airport_info = get_airport_coordinates(aeroporto)
        if airport_info:
            airport_name.append(airport_info["name"])
            airport_lat.append(airport_info["lat"])
            airport_lon.append(airport_info["lon"])
    return pd.DataFrame({'name': airport_name, 'lat': airport_lat, 'lon': airport_lon})

def create_dataframe_pandas_to_visualize_nmaxdestfrequenti(dest_numvoli, nummaxfrequenti=5):
    dict_ord = sorted(dest_numvoli.items(), key=lambda x: x[1], reverse=True)[:nummaxfrequenti]
    citta = [x for (x, y) in dict_ord]
    valore = [y for (x, y) in dict_ord]

    df_5max = pd.DataFrame({"Destinazione": citta, "Numvoli": valore})
    df_5max.set_index("Destinazione", inplace=True)
    return df_5max

def create_dataframe_pandas_to_visualize_aeroportiCitta_num_voliPartenzeArrivi(aeroporti_numvoli):
    df_pandas = pd.DataFrame.from_dict(aeroporti_numvoli, orient='index',
                                       columns=['Numero partenze', 'Numero arrivi'])
    return df_pandas
