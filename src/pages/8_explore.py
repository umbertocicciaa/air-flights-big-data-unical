import os
import streamlit as st
from ..utils.datasets import read_parquet

hdfs_input_path = os.getenv("HDFS_OUTPUT_PATH", "/outputs")


def explore_data():
    st.title("Explore Data")

    data = read_parquet(hdfs_input_path)

    if data is not None:
        st.write("Data Overview:")
        st.dataframe(data.head())

        st.write("Summary Statistics:")
        st.write(data.describe())

        st.write("Select a column to visualize:")
        column = st.selectbox("Column", data.columns)

        if column:
            st.bar_chart(data[column].value_counts())
    else:
        st.error("Failed to load data.")


explore_data()
