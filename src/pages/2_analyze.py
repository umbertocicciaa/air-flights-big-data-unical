import streamlit as st
from pyspark.sql.functions import col, count
from utils.datasets import read_parquet


#hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")


def analyze_data(dataframe):
    if st.checkbox("Show Summary Statistics"):
        st.write(dataframe.describe())

    st.sidebar.header("Filter Options")
    column_to_filter = st.sidebar.selectbox("Select Column to Filter", dataframe.columns)
    filter_value = st.sidebar.text_input("Enter Value to Filter")

    if filter_value:
        filtered_data = dataframe.filter(dataframe[column_to_filter].cast("string") == filter_value)
        st.write("Filtered Data", filtered_data)

    st.sidebar.header("Visualization Options")
    if st.sidebar.button("Show Histogram"):
        column_to_plot = st.sidebar.selectbox("Select Column for Histogram", dataframe.columns)
        dataset = dataframe[column_to_plot]
        if dataset is not None:
            value_counts = dataframe.groupBy(col(column_to_plot)).agg(count("*").alias("count")).toPandas()
            st.bar_chart(value_counts.set_index(column_to_plot))


st.title("Data Analysis")
#path =f"{hdfs_input_path}outputs"
path = "shared-filesystem/outputs"
data = read_parquet(path)
analyze_data(data)
