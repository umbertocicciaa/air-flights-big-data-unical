import pandas as pd
import streamlit as st
import plotly.express as px

from utils.utils import get_city_coordinate, get_airport_coordinates, get_sorted_city_list
from query.query import query_numero_partenze_e_arrivi_citta, query_ritardo_medio_partenza_arrivo_citta, query_destinazione_numvoli_citta, query_citta_numvoli_aeroporto


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


st.set_page_config(page_title="Airport statistics", layout="wide")
st.title(":blue[Airport statistics]")

st.markdown("""
Welcome to the section dedicated to the analysis of airport statistics.
Here you can select your city of interest and view useful information such as the number of departing and arriving flights, average delays recorded and the most popular destinations.""")

with st.expander("More information"):
    st.markdown("""
    Key Features:
    - :blue-background[Air Traffic Metrics]: Discover the total number of flights departing and arriving for the selected city.

    - :blue-background[Delay Analysis]: View the average delays of departing and arriving flights through intuitive graphs.

    - :blue-background[Air Traffic Analysis by Airport]: View the number of flights departing and arriving for each airport belonging to the selected city.

    - :blue-background[Most Popular Destinations]: Explore the most frequent destinations with up to 10 locations, represented in an interactive bar graph.
    - :blue-background[Destination Map]: View the destination locations of flights departing from the selected city on the map.
    """)

lista_ordinata_citta = get_sorted_city_list()

citta = st.sidebar.selectbox('Select a city', lista_ordinata_citta, index=None)

nmaxfreq = st.sidebar.select_slider("Select the number of most frequent destinations to display",
                                    options=[None] + [i for i in range(1, 11)])

visualizza = False
if (citta and nmaxfreq):
    visualizza = st.sidebar.button("Calculate")

if visualizza:
    a, b = st.columns(2)
    numvoli_partenza, numvoli_arrivo = query_numero_partenze_e_arrivi_citta(citta)

    a.metric("Number of departures", numvoli_partenza, border=True)
    b.metric("Number of arrivals", numvoli_arrivo, border=True)

    lista_ritardi = query_ritardo_medio_partenza_arrivo_citta(citta)
    chart_ritardi_data = create_dataframe_pandas_to_visualize_delays(lista_ritardi)
    st.markdown("### :blue[Average Delays for Departures and Arrivals]")
    st.bar_chart(chart_ritardi_data)

    aeroporti_numvoli = query_citta_numvoli_aeroporto(citta)
    aerorti_num_voli_pd = create_dataframe_pandas_to_visualize_aeroportiCitta_num_voliPartenzeArrivi(aeroporti_numvoli)
    st.markdown("### :blue[Air Traffic Analysis for City Airport]")
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(aerorti_num_voli_pd, use_container_width=True)
    with col2:
        df_airport_name_coordinates = create_dataframe_pandas_to_visualize_map_airports_coordinates(
            aeroporti_numvoli.keys())

        fig = px.scatter_mapbox(
            df_airport_name_coordinates,
            lat='lat',
            lon='lon',
            hover_name='name',
            zoom=9
        )

        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        st.plotly_chart(fig, use_container_width=True)

    dest_numvoli = query_destinazione_numvoli_citta(citta)
    chart_destmaxfreq_data = create_dataframe_pandas_to_visualize_nmaxdestfrequenti(dest_numvoli, nmaxfreq)
    st.markdown("### :blue[Most Popular Destinations]")
    st.bar_chart(chart_destmaxfreq_data, horizontal=True)

    destinazioni = list(dest_numvoli.keys())
    st.markdown(f"### :blue[Possibile destination from: {citta}]")
    fig = px.scatter_mapbox(
        create_dataframe_pandas_to_visualize_city_coordinates(destinazioni),
        lat='lat',
        lon='lon',
        hover_name='name',
        height=600,
        zoom=3
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)
