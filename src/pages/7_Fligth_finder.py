from datetime import date, time

import airportsdata
import pandas as pd
import pydeck as pdk
import streamlit as st
from geopy.distance import geodesic
from pyspark.sql import DataFrame
from pyspark.sql.types import Row
from query.query import query_get_volo
from query.route.find_flight import get_flight_advanced_delay, get_flight_advanced_canc, get_flight_advanced_div
from utils.utils import get_coordinates_city, get_sorted_city_list
from logs.logger import logger

def build_map(origin_par: str, destinazione: str):
    origin = get_coordinates_city(origin_par)
    destination = get_coordinates_city(destinazione)

    if origin is None or destination is None:
        st.error("Error: Unable to find coordinates for the specified cities.")
        return

    distance_km = geodesic(origin, destination).kilometers

    midpoint = (
        (origin[0] + destination[0]) / 2,
        (origin[1] + destination[1]) / 2,
    )

    points = pd.DataFrame([
        {"name": "Origin", "latitude": origin[0], "longitude": origin[1]},
        {"name": "Destination", "latitude": destination[0], "longitude": destination[1]},
    ])

    texts = pd.DataFrame([
        {"text": f"{distance_km:.1f} km", "latitude": midpoint[0], "longitude": midpoint[1]}
    ])

    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=points,
            get_position=["longitude", "latitude"],
            get_color="[200, 30, 0, 160]",
            get_radius=10_000,
        ),
        pdk.Layer(
            "LineLayer",
            data=[{"start": [origin[1], origin[0]], "end": [destination[1], destination[0]]}],
            get_source_position="start",
            get_target_position="end",
            get_color="[30, 144, 255]",
            get_width=4,
        ),
        pdk.Layer(
            "TextLayer",
            data=texts,
            get_position=["longitude", "latitude"],
            get_text="text",
            get_size=24,
            get_color="[30, 144, 255]",
            get_alignment_baseline="'bottom'",
        ),
    ]

    view_state = pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=4,
        pitch=50,
    )

    st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view_state))


aereoporti = airports = airportsdata.load('IATA')


def make_delay_plot(row: Row):
    val = (row["CarrierDelay"], row["WeatherDelay"], row["NASDelay"], row["SecurityDelay"], row["LateAircraftDelay"])
    if all(v is not None for v in val):
        data = pd.DataFrame({
            "Type of delay": ["CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"],
            "Minutes": val})
        st.markdown("#### :blue[Causes of the delay]")
        st.bar_chart(data.set_index("Type of delay")["Minutes"])


def visualizza_dir(row: Row):
    for i in range(1, 6):
        if row[f"Div{i}Airport"] is not None:
            aereoporto = aereoporti[row[f"Div{i}Airport"]]["name"]
            st.metric("Airport hijacking", aereoporto, border=True)
    if row["DivReachedDest"] == 1.0:
        st.markdown("### :blue[THE PLANE HAS REACHED ITS FINAL DESTINATION]")


def visualizzazione_singola(row: Row):
    if row["Cancelled"] == 1:
        st.markdown("# :red[FLIGHT CANCELLED!]")
        return
    aereoportoOr = aereoporti[row["Origin"]]["name"]
    aereoportoDest = aereoporti[row["Dest"]]["name"]

    st.markdown("### :blue[Geographic information]")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Departure airport", aereoportoOr, border=True)
    with col2:
        st.metric("Destination airport", aereoportoDest, border=True)

    st.markdown("### :blue[Flight Code]")
    st.metric("Flight Code", row["Flight_Number_Reporting_Airline"], border=True)

    if row["Diverted"] == 1:
        st.markdown("# :red[DIVERTED FLIGTH]")
        col4, col5 = st.columns(2)
        with col4:
            st.metric("Scheduled departure time", row["CRSDepTime"].strftime("%H:%M"), border=True)
        with col5:
            st.metric("Scheduled arrival time", row["CRSArrTime"].strftime("%H:%M"), border=True)
        st.markdown("### :blue[Airports where the flight was diverted]")
        visualizza_dir(row)
        return

    st.markdown("### :blue[Hourly information]")
    col6, col7, col8, col9 = st.columns(4)
    
    crsdeeptime = f"{row['CRSDepTime'] // 100:02}:{row['CRSDepTime'] % 100:02}"
    crsarrtime = f"{row['CRSArrTime'] // 100:02}:{row['CRSArrTime'] % 100:02}"
    deeptime = f"{row['DepTime'] // 100:02}:{row['DepTime'] % 100:02}"
    arrtime = f"{row['ArrTime'] // 100:02}:{row['ArrTime'] % 100:02}"
    
    with col6:
        st.metric("Scheduled departure time", crsdeeptime, delta=0, delta_color="off",
                  border=True)
    with col7:
        st.metric("Actual departure time", deeptime, delta=row["DepDelay"],
                  delta_color="inverse", border=True)
    with col8:
        st.metric("Scheduled arrival time", crsarrtime, delta=0, delta_color="off",
                  border=True)
    with col9:
        st.metric("Actual arrival time", arrtime, delta=row["ArrDelay"], delta_color="inverse",
                  border=True)

    st.markdown("### :blue[Delay information]")
    col8, col9 = st.columns(2)
    minRit = row["ArrDelayMinutes"]
    if minRit is not None:
        with col8:
            st.metric("Minutes late", f"{minRit} min", border=True)
        if minRit > 0:
            with col9:
                make_delay_plot(row)
        else:
            with col9:
                st.markdown("### :blue[The flight flew right on time]")
    else:
        st.markdown("#### :red[Information not available]")


def visualizza_informazioni(df: DataFrame):
    numVoli = df.count()
    if numVoli == 0:
        st.write("# :red[There is no flight for the information entered]")
        return
    volo = df.first()
    if volo is not None:
        visualizzazione_singola(volo)
    else:
        st.markdown("# :red[ERROR: No flight data available]")


def create_select_button(city: list):
    origine = st.selectbox("Choose origin", city, index=None)
    dest = st.selectbox("Choose destination", city, index=None)
    data = st.date_input("Enter departure date", date(2013, 1, 1))
    return origine, dest, data


def create_optinal_choose():
    opt = st.expander("Advanced search")
    with opt:
        senza_ritardo = st.checkbox("Exclude flights with delays")
        senza_cancellazioni = st.checkbox("Exclude cancelled flights")
        senza_dirottamenti = st.checkbox("Exclude hijacked flights")
    return senza_ritardo, senza_cancellazioni, senza_dirottamenti


st.set_page_config(page_title="Research", layout="wide")
st.title(":blue[FLIGTH FINDER]")

st.markdown(
    "Welcome to the flight search page! This interface allows you to perform advanced searches on flights and view useful details such as the route, any delays, cancellations and diversions."
)

with st.expander("more information"):
    st.markdown("""
   In the side panel you can:

    - Select the origin and destination from the list of available cities.
    - Indicate the desired departure date and time.
    - Start the search to obtain information on flights that match the entered criteria.

    You will be able to view the route map between the departure airport and the destination airport, which includes
    a visual indication of the total distance (in km).

    :blue-background[Basic information]

    - Departure and destination airport.
    - Departure and arrival times (scheduled and actual).
    - Causes of any delays.

    :blue-background[Management of Diverted or Cancelled Flights]

    - If the flight is diverted, displays the alternative airports to which it has been destined.
    - If the flight has been cancelled, an error message is displayed.
    """)

st.write("""---""")

st.title(":blue[START HERE]")

city = get_sorted_city_list()

origine, dest, data = create_select_button(city)

senza_ritardo, senza_cancellazioni, senza_dirottamenti = create_optinal_choose()
logger.info(f"Senza ritardo {senza_ritardo}, senza cancellazioni {senza_cancellazioni}, Senza dirottamenti {senza_dirottamenti}")
ricerca = False
if origine is not None and dest is not None:
    ricerca = st.button("FIND")

if ricerca and origine is not None and dest is not None:
    st.markdown(f"### :blue[Flight Path: {origine} ➡️ {dest}]")
    st.markdown("# :blue[Flight information]")
    logger.info(f"Searching flights for {data} from {origine} to {dest}")
    voli = query_get_volo(data, origine, dest)
    if senza_ritardo:
        voli = get_flight_advanced_delay(voli)
    if senza_cancellazioni:
        voli = get_flight_advanced_canc(voli)
    if senza_dirottamenti:
        voli = get_flight_advanced_div(voli)
    build_map(origine, dest)
    visualizza_informazioni(voli)