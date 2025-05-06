import streamlit as st
from utils.datasets import read_parquet


#hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")


def explore_data():
    st.title("Explore Data")

    #path =f"{hdfs_input_path}outputs"
    path ="shared-filesystem/outputs"
    data = read_parquet(path)
    if data is not None:
        st.write("Data Overview:")
        st.dataframe(data.limit(5))

        st.write("Summary Statistics:")
        st.dataframe(data.describe())

        st.write("Select a column to visualize:")
        column = st.selectbox("Column", data.columns)

        if column:
            column_data = data.groupBy(column).count()
            st.bar_chart(column_data)
    else:
        st.error("Failed to load data.")


explore_data()
