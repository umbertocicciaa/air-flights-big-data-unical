import streamlit as st
from utils.data_loader import load_parquet_data

def explore_data():
    st.title("Explore Data")
    
    data = load_parquet_data()
    
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

if __name__ == "__main__":
    explore_data()