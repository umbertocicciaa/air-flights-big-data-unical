import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from query.query import query_mesi_stato_voli, query_mesi_voli_settimana, query_citta_num_voli

mesi = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
        'november', 'december']


def create_dataframe_pandas_to_visualize_bargraph_status_numvoli(status_num_voli: list[list[int]]):
    in_orario = status_num_voli[0]
    cancellati = status_num_voli[1]
    dirottati = status_num_voli[2]
    in_ritardo = status_num_voli[3]

    dataframes = pd.DataFrame({
        'Month': mesi,
        'On time': in_orario,
        'Canceled': cancellati,
        'Diverted': dirottati,
        'Delayed': in_ritardo
    })
    return dataframes


st.set_page_config(page_title="Annual statistics", layout="wide")
st.title(":blue[Annual statistics]")

st.markdown("""

The page displays various analyses and graphical representations of air traffic, providing a complex overview of flight statistics.
The data is displayed in three main sections:

""")

with st.expander("maggiori informazioni"):
    st.markdown("""
    - :blue-background[Flight Status Bar Chart]: Displays the number of flights for each month of the year, broken down by flight status (on time, delayed, cancelled and diverted). This chart makes it easy to understand monthly trends and the distribution of different flight statuses.
    - :blue-background[Weekly Heat Map]: Displays the number of flights for each day of the week, broken down by month. Using a heat map helps you identify the busiest periods for the week and month, with a clear visual representation of weekly fluctuations.
    - :blue-background[Geographic Flight Map by City]: Represents the distribution of flights in the busiest cities. Each city is represented by a marker that varies in size and color based on the number of flights, providing a geographical overview of air traffic at a national level.

    This combination of charts provides a clear and detailed visualization of air traffic information, useful for analyzing and comparing flight data in a dynamic and interactive way.
    """)


num_voli_stato_volo = query_mesi_stato_voli()
df = create_dataframe_pandas_to_visualize_bargraph_status_numvoli(num_voli_stato_volo)
list_df_columns = list(df.columns)


fig1 = px.bar(df,
              x=list_df_columns[0],
              y=list_df_columns[1:],
              labels={"value": "Number of flights", "variable": "Flight status"},
              barmode="stack")

fig1.update_layout(
    xaxis_title=dict(text="Month", font=dict(weight="bold")),
    yaxis_title=dict(text="Number of flights", font=dict(weight="bold")),
    legend_title=dict(text="<b>Flight status</b>")
)

st.markdown("### :blue[Flight Status Bar Graph]")
st.plotly_chart(fig1)


data_mese_numvolisettimana = query_mesi_voli_settimana()

fig2 = px.imshow(data_mese_numvolisettimana,
                 labels=dict(x="Month", y="Day Week", color="Number of Flights"),
                 x=mesi,
                 y=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                 )

fig2.update_layout(
    xaxis_title=dict(text="Month", font=dict(weight="bold")),
    yaxis_title=dict(text="Day Week", font=dict(weight="bold")),
    coloraxis_colorbar=dict(title=dict(text="Number of Flights", font=dict(weight="bold"))),
    width=2000,
    height=550 
)

st.markdown("""### :blue[Weekly heat map]""")
st.plotly_chart(fig2)


df = query_citta_num_voli()
df['text'] = df['city'] + ' traffic: ' + df['num'].astype(str)
fig3 = go.Figure(data=go.Scattergeo(
    locationmode='country names',
    lon=df['lon'],
    lat=df["lat"],
    text=df['text'],
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
                text="Total flights to each city"
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

st.markdown("""### :blue[Geographic map of flights by city]""")

a, b = st.columns(2)

df1 = df[["city", "num"]]
with a:
    st.dataframe(df1.sort_values(by=["num"], ascending=False))

with b:
    st.plotly_chart(fig3)
