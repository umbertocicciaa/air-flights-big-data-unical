import pandas as pd
import streamlit as st
import plotly.express as px
from utils.utils import get_city_coordinate, get_airport_coordinates,getSortedListaCitta
from query.query import query_numero_partenze_e_arrivi_citta, query_ritardo_medio_partenza_arrivo_citta, query_destinazione_numvoli_citta, query_citta_numvoli_aeroporto

def create_dataframe_pandas_to_visualize_delays(lista_ritardi):
    df= pd.DataFrame({'ritardi partenze':lista_ritardi[0],'ritardi arrivi':lista_ritardi[1]})
    df.index= range(1,13)
    return df

def create_dataframe_pandas_to_visualize_city_coordinates(lista_citta):
    cities=[]
    latitudine=[]
    longitudine=[]
    dict_citta_coordinate= get_city_coordinate()
    for citta in lista_citta:
        if citta in dict_citta_coordinate:
            coordinates=dict_citta_coordinate[citta]
            cities.append(citta)
            latitudine.append(coordinates[0])
            longitudine.append(coordinates[1])
    return pd.DataFrame({"name":cities, 'lat': latitudine, 'lon': longitudine})

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


st.set_page_config(page_title="Statistiche aeroporti",layout="wide")
st.title(":blue[Statistiche aeroporti]")

st.markdown("""
Benvenuto nella sezione dedicata all'analisi delle statistiche aeroportuali. 
Qui puoi selezionare la tua città di interesse e visualizzare informazioni utili come il numero di voli in partenza e in arrivo, i ritardi medi registrati e le destinazioni più frequentate.""")

with st.expander("maggiori informazioni"):
    st.markdown("""
    Funzionalità principali:
    - :blue-background[Metriche di traffico aereo]: scopri il numero totale di voli in partenza e in arrivo per la città selezionata.
    
    - :blue-background[Analisi dei ritardi]: visualizza i ritardi medi dei voli in partenza e in arrivo tramite grafici intuitivi.
    
    - :blue-background[Analisi del Traffico Aereo per Aeroporto]: visualizza il numero di voli in partenza e arrivo per ciascun aeroporto appartenente alla citta selezionata.
    
    - :blue-background[Destinazioni più popolari]: esplora le destinazioni più frequenti con un massimo di 10 località, rappresentate in un grafico a barre interattivo.
    - :blue-background[Mappa delle destinazioni]: osserva sulla mappa le località di destinazione dei voli in partenza dalla città scelta.
    
    """)

lista_ordinata_citta=getSortedListaCitta()

citta = st.sidebar.selectbox('Seleziona una città', lista_ordinata_citta, index=None)
# seleziono il numero di destinazioni piu frequenti da visualizzare nel grafico a  barre.
nmaxfreq = st.sidebar.select_slider("Seleziona il numero di destinazioni piu frequenti da visualizzare",
                            options=[None] + [i for i in range(1, 11)])

visualizza=False
if(citta and nmaxfreq):
    visualizza=st.sidebar.button("Calcola")

if visualizza :

    
    a, b = st.columns(2)
    numvoli_partenza, numvoli_arrivo= query_numero_partenze_e_arrivi_citta(citta)

    a.metric("Numero partenze",numvoli_partenza,border=True)
    b.metric("Numero arrivi ", numvoli_arrivo, border=True)

    
    lista_ritardi= query_ritardo_medio_partenza_arrivo_citta(citta)
    chart_ritardi_data= create_dataframe_pandas_to_visualize_delays(lista_ritardi)
    st.markdown("### :blue[Ritardi Medi per Partenze e Arrivi]")
    st.bar_chart(chart_ritardi_data)


    aeroporti_numvoli= query_citta_numvoli_aeroporto(citta)
    aerorti_num_voli_pd=create_dataframe_pandas_to_visualize_aeroportiCitta_num_voliPartenzeArrivi(aeroporti_numvoli)
    st.markdown("### :blue[Analisi del Traffico Aereo per Aeroporto della Città]")
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


    dest_numvoli= query_destinazione_numvoli_citta(citta)
    chart_destmaxfreq_data= create_dataframe_pandas_to_visualize_nmaxdestfrequenti(dest_numvoli, nmaxfreq)
    st.markdown("### :blue[Destinazioni Più Frequenti]")
    st.bar_chart(chart_destmaxfreq_data,horizontal=True)


    destinazioni = list(dest_numvoli.keys())
    st.markdown(f"### :blue[Possibili destinazioni da: {citta}]")
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









