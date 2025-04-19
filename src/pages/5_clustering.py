import streamlit as st
import plotly.express as px
from query.query import build_month_dataframe, clustering_flights, preprocessing_clustering
from utils.utils import month_from_number


def view_clustering_k(dataframes, k_centr):
    dict_result_clustering = clustering_flights(dataframes, k_centr)
    clusteredData = dict_result_clustering["clusteredData"]
    silhouettes = dict_result_clustering["silhouette"]

    df_clusterPoint = clusteredData.groupby('cluster').size().rename('NumeroVoli')

    figs = px.scatter(
        clusteredData,
        x="ArrDelay",
        y="flight_duration",
        color='cluster',
        labels={"cluster": "Cluster"},
    )
    fig1 = px.bar(df_clusterPoint, x='NumeroVoli', y=df_clusterPoint.index,
                  orientation='h')

    fig1.update_layout(yaxis=dict(tickmode='linear'))
    return figs, fig1, silhouettes


mesi = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
        'november', 'december']

st.set_page_config(page_title="Clustering", layout="wide")
st.title(":blue[Visualizzazione del Clustering K-means]")
st.write(":blue[Questa pagina mostra la visualizzazione del clustering K-means per diverse configurazioni di 'k'.]")

mese = st.sidebar.selectbox('Seleziona un mese', mesi, index=None)

if mese:
    mese_number = int(month_from_number(mese))
    df = build_month_dataframe(mese_number)
    df_subsets = df.sample(fraction=0.25)
    df_clustering = preprocessing_clustering(df_subsets)
    k_values = [2, 3, 4, 5]

    for k in k_values:
        fig, fig_numPoints, silhouette = view_clustering_k(df_clustering, k)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f":blue[Clustering with k={k}]")
            st.plotly_chart(fig)
            st.metric(label="Factor di Silhouette", value=f"{silhouette:.4f}", border=True)
        with col2:
            st.subheader(f":blue[Cluster distribution(k={k})]")
            st.plotly_chart(fig_numPoints)
