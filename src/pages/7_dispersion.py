import os

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils.datasets import read_parquet

hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/outputs/")

st.title("Dispersion Graphs")

data = read_parquet(hdfs_input_path)

if data is not None:

    st.write("Dispersion Plot:")
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    selected_x = st.selectbox("Select X-axis variable", numeric_columns)
    selected_y = st.selectbox("Select Y-axis variable", numeric_columns)
    
    if st.button("Generate Dispersion Plot"):
        fig, ax = plt.subplots()
        sns.scatterplot(x=data[selected_x], y=data[selected_y], ax=ax)
        st.pyplot(fig)