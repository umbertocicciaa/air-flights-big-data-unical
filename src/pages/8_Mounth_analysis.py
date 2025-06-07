import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from query.dashboard_analysis.avg_analysis_flights import calculate_monthly_flight_statistics
from query.dashboard_analysis.fligth_delays_cause import causes_delay
from query.dashboard_analysis.fligth_infos import monthly_flight_statistics
from query.dashboard_analysis.range_delay import calculateFlightDelayRange
from query.query import build_month_dataframe

mesi = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
        'november', 'december']

st.set_page_config(page_title="Monthly statistics", layout="wide")
st.header(":blue[Monthly statistics]")

st.title(":blue[Monthly statistics]")

st.markdown(
"This platform allows you to explore flight data for a specific "
":blue-background[month] in an intuitive and interactive way.")

with st.expander("more information"):
    st.markdown('''
        Through clear graphs and detailed metrics, you can analyze:
        - Total number of flights
        - Average delay
        - Average distance traveled
        - Average flight duration

        In addition, you will find:
        - A classification of delays in time bands.
        - An overview of the status of flights (on time, cancelled, diverted, delayed).
        - The main causes of delays represented graphically.

        Discover monthly trends and get a complete and detailed view of monthly air traffic!
    ''')

mese = st.selectbox('Select a month', mesi, index=None)

if mese:
    mese_numero = mesi.index(mese) + 1
    df_mese = build_month_dataframe(mese_numero)
    lista_avg = calculate_monthly_flight_statistics(df_mese)

    a, b = st.columns(2)
    c, d = st.columns(2)

    if mese == "january":
        a.metric("Number of flights", lista_avg[0], delta=0.0, delta_color="off", border=True)
        b.metric("Average delay", f"{lista_avg[1]} min", delta=0.0, delta_color="off", border=True)
        c.metric("Average distance", f"{lista_avg[2]} miglia", delta=0.0, delta_color="off", border=True)
        d.metric("Average flight minutes", f"{lista_avg[3]} min", delta=0.0, delta_color="off", border=True)

    else:
        mese_precedente = 12 if mese_numero == 1 else mese_numero - 1
        df_mese_precedente = build_month_dataframe(mese_precedente)
        lista_avg_precedente = calculate_monthly_flight_statistics(df_mese_precedente)
        pernumvoli = round((((lista_avg[0] - lista_avg_precedente[0]) / lista_avg_precedente[0]) * 100), 2)
        perritardomedio = round((((lista_avg[1] - lista_avg_precedente[1]) / lista_avg_precedente[1]) * 100), 2)
        perdistanzamedia = round((((lista_avg[2] - lista_avg_precedente[2]) / lista_avg_precedente[2]) * 100), 2)
        permediaminutivolo = round((((lista_avg[3] - lista_avg_precedente[3]) / lista_avg_precedente[3]) * 100), 2)
        a.metric("Number of flights", lista_avg[0], delta=f"{pernumvoli} %", border=True)
        b.metric("Average delay", f"{lista_avg[1]} min", delta=f"{perritardomedio} %", border=True)
        c.metric("Average distance", f"{lista_avg[2]} miglia", delta=f"{perdistanzamedia} %", border=True)
        d.metric("Average flight minutes", f"{lista_avg[3]} min", delta=f"{permediaminutivolo} %", border=True)

    categorie = ["0-15", "16-30", "31-45", "46-60", "60+"]
    range_ritardi = calculateFlightDelayRange(df_mese)

    df_bar = pd.DataFrame({
        "Categories": categorie,
        "Delays": range_ritardi
    })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""### :blue[Classification of delays in time bands]""")
        st.bar_chart(df_bar.set_index("Categories")["Delays"])

    with col2:
        info_voli_mese = monthly_flight_statistics(df_mese)
        labels = ['Time', 'Canceled', 'Diverted', 'Delays']

        fig = go.Figure(
            data=[go.Pie(labels=labels, values=info_voli_mese, hole=0.3, domain={'x': [0, 1], 'y': [0, 1]})])

        fig.update_traces(textinfo='percent+label',
                          pull=[0.1, 0.3, 0.3, 0.1])

        st.markdown("""### :blue[Flight status]""")
        st.plotly_chart(fig)

    cause_ritardi = causes_delay(df_mese)
    df_cause_ritardi = pd.DataFrame(list(cause_ritardi.items()), columns=['Cause', 'Number of Delays'])

    st.markdown("""### :blue[Main causes of delays]""")
    st.bar_chart(df_cause_ritardi.set_index('Cause'), horizontal=True)
