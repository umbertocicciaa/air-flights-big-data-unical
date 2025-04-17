import streamlit as st

def main():
    st.title("Home")
    st.write("This application allows you to explore and analyze data in Parquet format.")
    
    st.header("Navigation")
    st.write("Use the sidebar to navigate to different pages:")
    st.write("- Explore: Dive into the dataset and visualize the data.")
    st.write("- Analyze: Perform statistical analysis and data filtering.")

if __name__ == "__main__":
    main()