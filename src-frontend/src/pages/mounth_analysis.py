import pandas as pd
import streamlit as st
from query.query import build_month_dataframe
from query.dashboard_analysis.avg_analysis_flights import calculate_monthly_flight_statistics
from query.dashboard_analysis.fligth_delays_cause import causes_delay
from query.dashboard_analysis.fligth_infos import monthly_flight_statistics
from query.dashboard_analysis.range_delay import calculateFlightDelayRange
from utils.utils import month_from_number, previous_month
import plotly.graph_objects as go


mesi= ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno','luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

st.set_page_config(page_title="Statistiche mensili",layout="wide")
st.sidebar.header(":blue[Statistiche mensili]")

st.title(":blue[Statistiche mensili]")

st.markdown("Questa piattaforma ti permette di esplorare in modo intuitivo e interattivo i dati relativi ai voli per un :blue-background[mese] specifico.")
with st.expander("maggiori informazioni"):
    st.markdown('''
        Attraverso grafici chiari e metriche dettagliate, puoi analizzare:
        - Numero totale di voli
        - Ritardo medio
        - Distanza media percorsa
        - Durata media dei voli
        
        Inoltre, troverai:
        - Una classificazione dei ritardi in fasce temporali.
        - Una panoramica dello stato dei voli (in orario, cancellati, dirottati, in ritardo).
        - Le principali cause dei ritardi rappresentate graficamente.
        
        Scopri le tendenze mensili e ottieni una visione completa e dettagliata del traffico aereo mensile!
    ''')

mese = st.sidebar.selectbox('Seleziona un mese',mesi,index=None)


if mese:
    df_mese= build_month_dataframe(month_from_number(mese))
    lista_avg = calculate_monthly_flight_statistics(df_mese)

    # PARTE 1
    # Colonne per le metriche
    a, b = st.columns(2)
    c, d = st.columns(2)

    if(mese=="gennaio"):
        a.metric("Numero voli", lista_avg[0],delta=0.0,delta_color="off", border=True)
        b.metric("Ritardo medio", f"{lista_avg[1]} min",delta=0.0,delta_color="off",border=True)
        c.metric("Distanza media", f"{lista_avg[2]} miglia",delta=0.0, delta_color="off", border=True)
        d.metric("Media minuti di volo", f"{lista_avg[3]} min", delta=0.0, delta_color="off", border=True)


    else:
        df_mese_precedente = build_month_dataframe(month_from_number(previous_month(mese)))
        lista_avg_precedente = calculate_monthly_flight_statistics(df_mese_precedente)
        pernumvoli = round((((lista_avg[0] - lista_avg_precedente[0]) / lista_avg_precedente[0]) * 100), 2)
        perritardomedio = round((((lista_avg[1] - lista_avg_precedente[1]) / lista_avg_precedente[1]) * 100), 2)
        perdistanzamedia = round((((lista_avg[2] - lista_avg_precedente[2]) / lista_avg_precedente[2]) * 100), 2)
        permediaminutivolo = round((((lista_avg[3] - lista_avg_precedente[3]) / lista_avg_precedente[3]) * 100), 2)
        a.metric("Numero voli", lista_avg[0], delta=f"{pernumvoli} %", border=True)
        b.metric("Ritardo medio", f"{lista_avg[1]} min", delta=f"{perritardomedio} %", border=True)
        c.metric("Distanza media", f"{lista_avg[2]} miglia", delta=f"{perdistanzamedia} %", border=True)
        d.metric("Media minuti di volo", f"{lista_avg[3]} min", delta=f"{permediaminutivolo} %", border=True)


    #PARTE 2
    # Creazione delle categorie di ritardi
    categorie = ["0-15", "16-30", "31-45", "46-60", "60+"]
    range_ritardi = calculateFlightDelayRange(df_mese)

    # Creazione di un DataFrame pandas per il grafico a barre
    df_bar = pd.DataFrame({
        "Categorie": categorie,
        "Ritardi": range_ritardi
    })

    # Creazione di due colonne con la stessa altezza
    col1, col2 = st.columns(2)  # Due colonne di uguale larghezza

    with col1:
        # Grafico a barre
        st.markdown("""### :blue[Classificazione dei ritardi in fasce temporali]""")
        st.bar_chart(df_bar.set_index("Categorie")["Ritardi"])

    with col2:
        # Dati per il grafico a torta
        info_voli_mese = monthly_flight_statistics(df_mese)
        labels = ['Orario', 'Cancellati', 'Dirottati', 'Ritardi']

        fig = go.Figure(
            data=[go.Pie(labels=labels, values=info_voli_mese, hole=0.3, domain={'x': [0, 1], 'y': [0, 1]})])

        # Modifica della dimensione della torta
        fig.update_traces(textinfo='percent+label',
                          pull=[0.1, 0.3, 0.3, 0.1])  # Aggiungere una leggera separazione per evidenziare

        st.markdown("""### :blue[Stato dei voli]""")
        st.plotly_chart(fig)

    #PARTE 3

    cause_ritardi= causes_delay(df_mese)
    # Convertiamo il dizionario in un DataFrame
    df_cause_ritardi = pd.DataFrame(list(cause_ritardi.items()), columns=['Causa', 'Numero di Ritardi'])

    st.markdown("""### :blue[Principali cause dei ritardi]""")
    # Utilizziamo st.bar_chart per mostrare il grafico
    st.bar_chart(df_cause_ritardi.set_index('Causa'),horizontal=True)

