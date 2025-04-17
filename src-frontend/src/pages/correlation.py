import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from services.data_loader import load_parquet_data

st.title("Correlation Graphs")

data = load_parquet_data()

if data is not None:

    if st.button("Generate Correlation Matrix"):
        st.write("Correlation Matrix:")
        corr_matrix = data.corr()
        st.write(corr_matrix)

        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, ax=ax)
        st.pyplot(fig)