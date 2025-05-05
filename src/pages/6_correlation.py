import os

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from utils.datasets import read_parquet

#hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")

st.title("Correlation Graphs")

#path =f"{hdfs_input_path}outputs"
path ="shared-filesystem/outputs"
data = read_parquet(path)
st.write("Select two columns to calculate correlation:")
col1 = st.selectbox("Select first column:", data.columns)
col2 = st.selectbox("Select second column:", data.columns)

if data is not None:

    if st.button("Generate Correlation Matrix"):
        st.write("Correlation Matrix:")
        numeric_cols = [col for col, dtype in data.dtypes if dtype in ('int', 'double')]
        corr_matrix = {col1: {col2: data.stat.corr(col1, col2) for col2 in numeric_cols} for col1 in numeric_cols}
        st.write(corr_matrix)

        fig, ax = plt.subplots()
        sns.heatmap(pd.DataFrame(corr_matrix), annot=True, ax=ax)
        st.pyplot(fig)
        
        st.write("Correlation Value:")
        correlation_value = data.stat.corr(col1, col2)
        st.write(f"Correlation between {col1} and {col2}: {correlation_value}")
    