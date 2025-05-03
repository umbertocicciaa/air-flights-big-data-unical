import os
import streamlit as st
from dotenv import load_dotenv

env_file = os.getenv("ENV", "./local.env")
load_dotenv(dotenv_path=env_file)


st.title("Home")
st.write("This application allows you to explore and analyze data in Parquet format.")
st.header("Navigation")
st.write("Use the sidebar to navigate to different pagess:")
st.write("- Explore: Dive into the dataset and visualize the data.")
st.write("- Analyze: Perform statistical analysis and data filtering.")