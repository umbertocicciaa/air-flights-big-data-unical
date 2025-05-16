from requests import get
import streamlit as st
from pyspark.sql.functions import col, count
from utils.datasets import read_parquet
from utils.session_redis import get_from_cache, save_to_cache

#hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")


def analyze_data(dataframe):
    if st.checkbox("Show Summary Statistics"):
        st.write(dataframe.describe())

    st.header("Filter Options")
    
    column_to_filter = get_from_cache('select_column_to_filter')
    filter_value     = get_from_cache('select_filter_value')
    
    if column_to_filter is None:
        column_to_filter = st.selectbox("Select Column to Filter", dataframe.columns)
    else:
        column_to_filter = st.selectbox("Select Column to Filter", dataframe.columns, index=dataframe.columns.index(column_to_filter))   
    save_to_cache('select_column_to_filter', column_to_filter, 3600)
    
    if filter_value is None:
        filter_value = st.text_input("Enter Value to Filter")
    else:
        filter_value = st.text_input("Enter Value to Filter", value=filter_value)    
    save_to_cache('select_filter_value', filter_value, 3600)

    if filter_value:
        if st.button("Filter data"):
            filtered_data = dataframe.filter(dataframe[column_to_filter].cast("string") == filter_value)
            st.write("Filtered Data", filtered_data)

    st.header("Visualization Options")
    if st.button("Show Histogram"):
        column_to_plot = st.selectbox("Select Column for Histogram", dataframe.columns)
        dataset = dataframe[column_to_plot]
        if dataset is not None:
            value_counts = dataframe.groupBy(col(column_to_plot)).agg(count("*").alias("count")).toPandas()
            st.bar_chart(value_counts.set_index(column_to_plot))


st.title("Data Analysis")
#path =f"{hdfs_input_path}outputs"
path = "shared-filesystem/outputs"
data = read_parquet(path)
analyze_data(data)
