import os

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils.datasets import read_parquet

# hdfs_input_path = os.getenv("HDFS_PATH", "hdfs://namenode:9000/")

st.title("Dispersion Graphs")

#path =f"{hdfs_input_path}outputs"
path ="shared-filesystem/inputs/"
files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.csv')]
dataframes = [pd.read_csv(file) for file in files]
data = pd.concat(dataframes, ignore_index=True)
st.write("Select two columns to calculate correlation:")
data = data.select_dtypes(include=['number'])
numeric_columns = data.select_dtypes(include=['number']).columns
selected_x = st.selectbox("Select X-axis variable", numeric_columns)
selected_y = st.selectbox("Select Y-axis variable", numeric_columns)

if data is not None and selected_x  and selected_y: 
    st.write("Dispersion Plot:")
    fig, ax = plt.subplots()
    sns.scatterplot(x=data[selected_x], y=data[selected_y], ax=ax)
    st.pyplot(fig)