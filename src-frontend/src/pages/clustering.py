import streamlit as st
import plotly.express as px
from query.query import build_month_dataframe, clusteringFlights, preprocessing_clustering
from utils.utils import month_from_number

def visualizza_clustering_k(df, k):
    dictResultClustring = clusteringFlights(df, k)
    clusteredData = dictResultClustring["clusteredData"]
    silhouette = dictResultClustring["silhouette"]
    centroids = dictResultClustring["centroids"]

    df_clusterPoint = clusteredData.groupby('cluster').size().rename('NumeroVoli')

    fig = px.scatter(
        clusteredData,
        x="ArrDelay",
        y="flight_duration",
        color='cluster',
        labels={"cluster": "Cluster"},
    )
    fig1 = px.bar(df_clusterPoint, x='NumeroVoli', y=df_clusterPoint.index,
                  orientation='h')

    fig1.update_layout(yaxis=dict(tickmode='linear'))
    return fig, fig1, silhouette

mesi= ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno','luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

st.set_page_config(page_title="Clustering", layout="wide")
st.title(":blue[Visualizzazione del Clustering K-means]")
st.write(":blue[Questa pagina mostra la visualizzazione del clustering K-means per diverse configurazioni di 'k'.]")

mese = st.sidebar.selectbox('Seleziona un mese',mesi,index=None)

if mese:

    df = build_month_dataframe(month_from_number(mese))
    df_sottoinsieme = df.sample(fraction=0.25)
    df_clustering = preprocessing_clustering(df_sottoinsieme)
    k_values = [2, 3, 4, 5]

    for k in k_values:
        fig, fig_numPoints, silhouette = visualizza_clustering_k(df_clustering, k)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f":blue[Clustering con k={k}]")
            st.plotly_chart(fig)
            st.metric(label="Coefficiente di Silhouette", value=f"{silhouette:.4f}",border=True)
        with col2:
            st.subheader(f":blue[Distribuzione dei Cluster (k={k})]")
            st.plotly_chart(fig_numPoints)
