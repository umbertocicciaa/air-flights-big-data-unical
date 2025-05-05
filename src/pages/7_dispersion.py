import os

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils.datasets import read_parquet

# hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")

st.title("Dispersion Graphs")

#path =f"{hdfs_input_path}outputs"
path ="shared-filesystem/outputs"
data = read_parquet(path)

if data is not None:
    numeric_columns = [col for col, dtype in data.dtypes if dtype in ('double', 'int')]

    st.write("Dispersion Plot:")
    selected_x = st.selectbox("Select X-axis variable", numeric_columns)
    selected_y = st.selectbox("Select Y-axis variable", numeric_columns)
    
    if st.button("Generate Dispersion Plot"):
        fig, ax = plt.subplots()
        sns.scatterplot(x=data[selected_x], y=data[selected_y], ax=ax)
        st.pyplot(fig)