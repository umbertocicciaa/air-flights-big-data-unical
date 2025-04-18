import os

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from utils.datasets import read_parquet

hdfs_input_path = os.getenv("HDFS_OUTPUT_PATH", "/outputs")

st.title("Correlation Graphs")

data = read_parquet(hdfs_input_path)

if data is not None:

    if st.button("Generate Correlation Matrix"):
        st.write("Correlation Matrix:")
        corr_matrix = data.corr()
        st.write(corr_matrix)

        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, ax=ax)
        st.pyplot(fig)