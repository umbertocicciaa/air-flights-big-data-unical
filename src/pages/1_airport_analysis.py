from operator import index
import plotly.express as px
import streamlit as st
from query.query import query_numero_partenze_e_arrivi_citta, query_ritardo_medio_partenza_arrivo_citta, \
    query_destinazione_numvoli_citta, query_citta_numvoli_aeroporto
from services.airport_analysis_service import create_dataframe_pandas_to_visualize_delays, \
    create_dataframe_pandas_to_visualize_city_coordinates, \
    create_dataframe_pandas_to_visualize_map_airports_coordinates, \
    create_dataframe_pandas_to_visualize_nmaxdestfrequenti, \
    create_dataframe_pandas_to_visualize_aeroportiCitta_num_voliPartenzeArrivi
from utils.utils import get_sorted_city_list
from utils.session_redis import get_client, get_from_cache, save_to_cache

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


redis_client = get_client()

citta = get_from_cache('select_city')
nmaxfreq = get_from_cache('select_nmaxfreq')

if citta is not None:
    citta = st.selectbox('Select a city', lista_ordinata_citta, index=lista_ordinata_citta.index(citta) if citta in lista_ordinata_citta else None)
else:
    citta = st.selectbox('Select a city', lista_ordinata_citta, index=None)
save_to_cache('select_city', citta, 3600)
    
options_nmaxfreq = [None] + [i for i in range(1, 11)]
if nmaxfreq is not None:
    nmaxfreq = st.select_slider(
        "Select the number of most frequent destinations to display",
        options=options_nmaxfreq,
        value=options_nmaxfreq.index(nmaxfreq)
    )
else:
    nmaxfreq = st.select_slider(
        "Select the number of most frequent destinations to display",
        options=options_nmaxfreq
    )
save_to_cache('select_nmaxfreq', nmaxfreq, 3600)


visualizza = False
if (citta and nmaxfreq):
    visualizza = st.button("Calculate")

if visualizza:
    a, b = st.columns(2)
    citta = str(citta)
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
    if nmaxfreq is not None:
        nmaxfreq = int(nmaxfreq)
    else:
        nmaxfreq = 0
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
