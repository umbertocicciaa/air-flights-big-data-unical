import datetime
import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from pyspark import Row
from pyspark.sql import DataFrame
import pydeck as pdk

from query.query import query_get_volo

from query.route.find_flight import get_flight_advanced_delay, get_flight_advanced_canc, get_flight_advanced_div
from utils.utils import get_coordinates_city, getSortedListaCitta


def build_map(origine : str, destinazione: str):
    # Ottieni le coordinate di origine e destinazione
    origin = get_coordinates_city(origine)
    destination = get_coordinates_city(destinazione)

    # Calcola la distanza tra i due punti
    distance_km = geodesic(origin, destination).kilometers

    # Calcola il punto medio tra origine e destinazione
    midpoint = (
        (origin[0] + destination[0]) / 2,
        (origin[1] + destination[1]) / 2,
    )

    # Crea un DataFrame per i punti
    points = pd.DataFrame([
        {"name": "Origin", "latitude": origin[0], "longitude": origin[1]},
        {"name": "Destination", "latitude": destination[0], "longitude": destination[1]},
    ])

    # Crea un DataFrame per il testo (posizionato al punto medio)
    texts = pd.DataFrame([
        {"text": f"{distance_km:.1f} km", "latitude": midpoint[0], "longitude": midpoint[1]}
    ])

    # Configurazione della mappa con Pydeck
    layers = [
        # Aggiunge un layer per i punti
        pdk.Layer(
            "ScatterplotLayer",
            data=points,
            get_position=["longitude", "latitude"],
            get_color="[200, 30, 0, 160]",
            get_radius=10_000,
        ),
        # Aggiunge un layer per la linea tra i due punti
        pdk.Layer(
            "LineLayer",
            data=[{"start": [origin[1], origin[0]], "end": [destination[1], destination[0]]}],
            get_source_position="start",
            get_target_position="end",
            get_color="[30, 144, 255]",
            get_width=4,
        ),
        # Aggiunge un layer per il testo (distanza)
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

    # Imposta la vista iniziale della mappa
    view_state = pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=4,
        pitch=50,
    )

    # Visualizza la mappa con Pydeck
    st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view_state))

aereoporti = airports = airportsdata.load('IATA')

def make_delay_plot(row: Row):
    val = (row["CarrierDelay"], row["WeatherDelay"],row["NASDelay"], row["SecurityDelay"],row["LateAircraftDelay"])
    if all(v is not None for v in val):
        data = pd.DataFrame({
            "Tipo di ritardo": ["CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"],
            "Minuti": val })
        st.markdown("#### :blue[Cause del ritardo]")
        st.bar_chart(data.set_index("Tipo di ritardo")["Minuti"])


def visualizza_dir(row: Row):
    for i in range(1,6):
        if row[f"Div{i}Airport"] is not None:
            aereoporto = aereoporti[row[f"Div{i}Airport"]]["name"]
            st.metric("Aereporto di dirottamento", aereoporto , border=True)
    if row["DivReachedDest"] == 1.0:
        st.markdown("### :blue[L'AEREO HA RAGGIUNTO LA DESTINAZIONE FINALE]")

def visualizzazione_singola(row: Row):
    if row["Cancelled"] == 1:
        st.markdown("# :red[VOLO CANCELLATO!]")
        return
    aereoportoOr = aereoporti[row["Origin"]]["name"]
    aereoportoDest = aereoporti[row["Dest"]]["name"]

    st.markdown("### :blue[Informazioni geografiche]")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Aereoporto di partenza", aereoportoOr, border=True)
    with col2:
        st.metric("Aereoporto di destinazione", aereoportoDest , border=True)

    st.markdown("### :blue[Codice di volo]")
    st.metric("Codice di volo", row["Flight_Number_Reporting_Airline"], border=True)

    if row["Diverted"] == 1:
        st.markdown("# :red[AEREO DIROTTATO]")
        col4, col5 = st.columns(2)
        with col4:
            st.metric("Orario di partenza schedulato", row["CRSDepTime"].strftime("%H:%M"), border=True)
        with col5:
            st.metric("Orario di arrivo schedulato", row["CRSArrTime"].strftime("%H:%M"), border=True)
        st.markdown("### :blue[Aereoporti in cui il volo è stato dirottato]")
        visualizza_dir(row)
        return

    st.markdown("### :blue[Informazioni orarie]")
    col6, col7, col8, col9 = st.columns(4)
    with col6:
        st.metric("Orario di partenza schedulato", row["CRSDepTime"].strftime("%H:%M"), delta=0, delta_color="off", border=True)
    with col7:
        st.metric("Orario di partenza effettivo", row["DepTime"].strftime("%H:%M"), delta = row["DepDelay"],delta_color="inverse", border=True)
    with col8:
        st.metric("Orario di arrivo schedulato", row["CRSArrTime"].strftime("%H:%M"),delta=0, delta_color="off",border=True)
    with col9:
        st.metric("Orario di arrivo effettivo", row["ArrTime"].strftime("%H:%M"), delta = row["ArrDelay"],delta_color="inverse", border=True)

    st.markdown("### :blue[Informazioni sui ritardi]")
    col8, col9 = st.columns(2)
    minRit = row["ArrDelayMinutes"]
    if minRit is not None:
        with col8:
            st.metric("Minuti di ritardo", f"{minRit} min", border=True)
        if minRit > 0:
            with col9:
                make_delay_plot(row)
        else:
            with col9:
                st.markdown("### :blue[Il volo ha viaggiato in perfetto orario]")
    else:
        st.markdown("#### :red[Informazioni non disponibili]")

def visualizza_informazioni(df: DataFrame):
    numVoli = df.count()
    if numVoli == 0:
        st.write("# :red[Non esiste nessun volo per le informazioni inserite]")
        return
    try:
        volo = df.first()
        visualizzazione_singola(volo)
    except Exception as e:
        print(e)
        st.markdown("# :red[ERRORE: Non è possibile visualizzare i dati]")



def create_select_button(city: list):
    #scelte obbligatorie
    origine = st.sidebar.selectbox("Scegliere origine", city, index= None)
    dest = st.sidebar.selectbox("Scegliere destinazione", city , index= None)
    data = st.sidebar.date_input("Inserire data di partenza", datetime.date(2013,1,1))
    orario = st.sidebar.time_input("Orario di partenza", datetime.time(0, 0))
    return origine, dest, data, orario

def create_optinal_choose():
    opt = st.sidebar.expander("Ricerca avanzata")
    with opt:
        senza_ritardo = st.checkbox("Escludi voli con ritardi")
        senza_cancellazioni = st.checkbox("Escludi voli cancellati")
        senza_dirottamenti = st.checkbox("Escludi voli dirottati")
    return senza_ritardo,senza_cancellazioni, senza_dirottamenti

st.set_page_config(page_title="Ricerca", layout="wide")
st.title(":blue[RICERCA IL VOLO]")

st.markdown("Benvenuto nella pagina di ricerca dei voli! Questa interfaccia consente di effettuare ricerche avanzate sui voli "
          "e di visualizzare dettagli utili come il percorso, eventuali ritardi, cancellazioni e dirottamenti.")

with st.expander("maggiori informazioni"):
    st.markdown("""
    Nel pannello laterale potrai:
    
    - Selezionare origine e destinazione dalla lista di città disponibili.
    - Indicare la data e l'orario di partenza desiderati.
    - Avviare la ricerca per ottenere informazioni sui voli che corrispondono ai criteri inseriti.

    Potrai visualizzare la mappa del percorso tra l'aeroporto di partenza e l'aeroporto di destinazione, che include
    un'indicazione visiva della distanza totale (in km).

    :blue-background[Informazioni di base]
    
    - Aeroporto di partenza e destinazione.
    - Orari di partenza e arrivo (schedulati ed effettivi).
    - Cause di eventuali ritardi.

    :blue-background[Gestione dei Voli Dirottati o Cancellati]
    
    - Se il volo è dirottato, visualizza gli aeroporti alternativi in cui è stato destinato.
    - Se il volo è stato cancellato, viene visualizzato un messaggio di errore.
    """)
st.write("""---""")

st.sidebar.title(":blue[INIZIA DA QUI]")

#va ordinata
city = getSortedListaCitta()

origine, dest, data, orario = create_select_button(city)

#scelte opzionali
# senza ritardo, senza dirottamenti, se dirottato stampa gli aereoporti di dirottamento, raggiunge destinazione
senza_ritardo, senza_cancellazioni, senza_dirottamenti = create_optinal_choose()
print(senza_ritardo,senza_cancellazioni,senza_dirottamenti)
ricerca = False
if origine is not None and dest is not None:
    ricerca = st.sidebar.button("CERCA")

if ricerca:
    st.markdown(f"### :blue[Percorso del Volo: {origine} ➡️ {dest}]")
    build_map(origine,dest)
    st.markdown("# :blue[Informazioni sul volo]")
    voli = query_get_volo(data, origine, dest, orario)
    voli.show()
    if senza_ritardo:
         voli = get_flight_advanced_delay(voli)
    if senza_cancellazioni:
         voli = get_flight_advanced_canc(voli)
    if senza_dirottamenti:
         voli = get_flight_advanced_div(voli)
    visualizza_informazioni(voli)
