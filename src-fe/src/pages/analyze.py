import streamlit as st
from utils.data_loader import load_parquet_data

def analyze_data(data):
    st.title("Data Analysis")
    
    if st.checkbox("Show Summary Statistics"):
        st.write(data.describe())
    
    st.sidebar.header("Filter Options")
    column_to_filter = st.sidebar.selectbox("Select Column to Filter", data.columns)
    filter_value = st.sidebar.text_input("Enter Value to Filter")
    
    if filter_value:
        filtered_data = data[data[column_to_filter].astype(str).str.contains(filter_value, na=False)]
        st.write("Filtered Data", filtered_data)
    
    st.sidebar.header("Visualization Options")
    if st.sidebar.button("Show Histogram"):
        column_to_plot = st.sidebar.selectbox("Select Column for Histogram", data.columns)
        st.bar_chart(data[column_to_plot].value_counts())

def main():
    st.title("Data Analysis")
    data = load_parquet_data() 
    analyze_data(data)

if __name__ == "__main__":
    main()