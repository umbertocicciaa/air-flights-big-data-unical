import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from services.data_loader import load_parquet_data

st.title("Dispersion Graphs")

data = load_parquet_data()

if data is not None:

    st.write("Dispersion Plot:")
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    selected_x = st.selectbox("Select X-axis variable", numeric_columns)
    selected_y = st.selectbox("Select Y-axis variable", numeric_columns)
    
    if st.button("Generate Dispersion Plot"):
        fig, ax = plt.subplots()
        sns.scatterplot(x=data[selected_x], y=data[selected_y], ax=ax)
        st.pyplot(fig)