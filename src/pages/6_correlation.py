import os

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from utils.datasets import read_parquet

#hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")

st.title("Correlation Graphs")

#path =f"{hdfs_input_path}outputs"
path ="shared-filesystem/inputs/"
files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.csv')]
dataframes = [pd.read_csv(file) for file in files]
data = pd.concat(dataframes, ignore_index=True)
st.write("Select two columns to calculate correlation:")
data = data.select_dtypes(include=['number'])
numeric_columns = data.select_dtypes(include=['number']).columns

if data is not None:

    if st.button("Generate Correlation Matrix"):
        st.write("Correlation Matrix:")
        corr_matrix = data.corr()
        st.write(corr_matrix)

        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, ax=ax)
        st.pyplot(fig)
    