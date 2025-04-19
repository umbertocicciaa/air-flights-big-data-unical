import pandas as pd
import streamlit as st
import plotly.express as px
from query.query import query_mesi_stato_voli, query_mesi_voli_settimana, query_citta_num_voli
import plotly.graph_objs as go

mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre",
        "Novembre", "Dicembre"]


def create_dataframe_pandas_to_visualize_bargraph_status_numvoli(status_num_voli: list[list[int]]):
    in_orario = status_num_voli[0]
    cancellati = status_num_voli[1]
    dirottati = status_num_voli[2]
    in_ritardo = status_num_voli[3]

    dataframes = pd.DataFrame({
        'Mese': mesi,
        'In orario': in_orario,
        'Cancellati': cancellati,
        'Dirottati': dirottati,
        'In ritardo': in_ritardo
    })
    return dataframes


# Imposta la configurazione della pagina
st.set_page_config(page_title="Statistiche annuali", layout="wide")
st.title(":blue[Statistiche annuali]")

st.markdown("""

La pagina visualizza diverse analisi e rappresentazioni grafiche relative al traffico aereo, offrendo una panoramica complessa delle statistiche sui voli.
I dati vengono mostrati in tre sezioni principali:
""")

with st.expander("maggiori informazioni"):
    st.markdown("""
    - :blue-background[Grafico a barre sullo stato dei voli]: Mostra il numero di voli per ciascun mese dell'anno, suddiviso per stato del volo (in orario, in ritardo, cancellato e dirottato). Questo grafico consente di comprendere facilmente le tendenze mensili e la distribuzione dei vari stati dei voli.
    - :blue-background[Mappa di calore settimanale]: Visualizza il numero di voli per ogni giorno della settimana, suddiviso per mese. L'uso di una mappa di calore aiuta a identificare i periodi di maggiore traffico settimanale e mensile, con una rappresentazione visiva chiara delle fluttuazioni settimanali.
    - :blue-background[Mappa geografica dei voli per città]: Rappresenta la distribuzione dei voli nelle città più trafficate. Ogni città è rappresentata da un marker che varia in dimensione e colore in base al numero di voli, offrendo una panoramica geografica sul traffico aereo a livello nazionale.
    
    Questa combinazione di grafici consente una visualizzazione chiara e dettagliata delle informazioni sul traffico aereo, utile per analizzare e confrontare i dati relativi ai voli in modo dinamico e interattivo.
    """)

# PARTE 1
num_voli_stato_volo = query_mesi_stato_voli()
df = create_dataframe_pandas_to_visualize_bargraph_status_numvoli(num_voli_stato_volo)
list_df_columns = list(df.columns)

# grafico a barre
fig1 = px.bar(df,
              x=list_df_columns[0],
              y=list_df_columns[1:],
              labels={"value": "Numero di voli", "variable": "Stato del volo"},
              barmode="stack")

fig1.update_layout(
    xaxis_title=dict(text="Mese", font=dict(weight="bold")),
    yaxis_title=dict(text="Numero di voli", font=dict(weight="bold")),
    legend_title=dict(text="<b>Stato del volo</b>"  # Testo della legenda in grassetto
                      )
)

st.markdown("### :blue[Grafico a barre sullo stato dei voli]")
st.plotly_chart(fig1)

# PARTE 2
data_mese_numvolisettimana = query_mesi_voli_settimana()

fig2 = px.imshow(data_mese_numvolisettimana,
                 labels=dict(x="Mese", y="Giorno Settimana", color="Numero Voli"),
                 x=mesi,
                 y=["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"],
                 )

fig2.update_layout(
    xaxis_title=dict(text="Mese", font=dict(weight="bold")),
    yaxis_title=dict(text="Giorno Settimana", font=dict(weight="bold")),
    coloraxis_colorbar=dict(title=dict(text="Numero Voli", font=dict(weight="bold"))),
    width=2000,  # Specifica la larghezza in pixel
    height=550  # Specifica l'altezza in pixel
)

st.markdown("""### :blue[Mappa di calore settimanale]""")
st.plotly_chart(fig2)

# PARTE 3
df = query_citta_num_voli()
df['testo'] = df['citta'] + ' traffico: ' + df['num'].astype(str)
fig3 = go.Figure(data=go.Scattergeo(
    locationmode='country names',
    lon=df['lon'],
    lat=df["lat"],
    text=df['testo'],
    mode='markers',
    marker=dict(
        size=8,
        opacity=0.8,
        reversescale=False,
        autocolorscale=False,
        symbol='square',
        line=dict(
            width=1,
            color='rgba(102, 102, 102)'
        ),
        colorscale='Blues',
        cmin=0,
        color=df["num"],
        cmax=df["num"].max(),
        colorbar=dict(
            title=dict(
                text="Voli totali per ogni città"
            )
        )
    )))

fig3.update_layout(
    geo=dict(
        scope='usa',
        projection_type='albers usa',
        showland=True,
        landcolor="rgb(250, 250, 250)",
        subunitcolor="rgb(217, 217, 217)",
        countrycolor="rgb(217, 217, 217)",
        countrywidth=0.5,
        subunitwidth=0.5
    ),
)

st.markdown("""### :blue[Mappa geografica dei voli per città]""")

a, b = st.columns(2)

df1 = df[["citta", "num"]]
with a:
    st.dataframe(df1.sort_values(by=["num"], ascending=False))

with b:
    st.plotly_chart(fig3)
