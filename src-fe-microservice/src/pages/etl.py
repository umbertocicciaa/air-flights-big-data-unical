import streamlit as st
import pandas as pd
import requests
from utils.redis_connection import init_redis

st.title("Air Flights ETL Process")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.write("CSV file loaded successfully!")

    if st.button("Start ETL Process"):

        response = requests.post("http://etl:5000/upload", json={"filename": uploaded_file.name})

        if response.status_code == 200:
            st.success("ETL process started successfully!")
            r = init_redis()

            output_file_path = f"/mnt/shared-filesystem/outputs/{uploaded_file.name}"
            with open(output_file_path, 'r') as file:
                etl_result = file.read()

            r.set(uploaded_file.name, etl_result)
            st.success("ETL process result inserted into Redis cache successfully!")
        else:
            st.error("Failed to start the ETL process.")