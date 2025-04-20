import os
import streamlit as st
from utils.datasets import read_parquet

hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")


def analyze_data(dataframe):
    if st.checkbox("Show Summary Statistics"):
        st.write(dataframe.describe())

    st.sidebar.header("Filter Options")
    column_to_filter = st.sidebar.selectbox("Select Column to Filter", dataframe.columns)
    filter_value = st.sidebar.text_input("Enter Value to Filter")

    if filter_value:
        filtered_data = dataframe[dataframe[column_to_filter].astype(str).str.contains(filter_value, na=False)]
        st.write("Filtered Data", filtered_data)

    st.sidebar.header("Visualization Options")
    if st.sidebar.button("Show Histogram"):
        column_to_plot = st.sidebar.selectbox("Select Column for Histogram", dataframe.columns)
        st.bar_chart(dataframe[column_to_plot].value_counts())


st.title("Data Analysis")
path =f"{hdfs_input_path}outputs"
data = read_parquet(path)
analyze_data(data)
