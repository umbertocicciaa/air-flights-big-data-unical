# Streamlit Multipage Microservice

This project is a Streamlit multipage microservice designed for exploring and analyzing data in Parquet format. It integrates with an ETL microservice to load and process data efficiently.

## Project Structure

```
streamlit-microservice
├── src
│   ├── pages
│   │   ├── home.py         # Home page with introduction and navigation
│   │   ├── explore.py      # Page for exploring data in Parquet format
│   │   └── analyze.py      # Page for performing data analysis
│   ├── utils
│   │   └── data_loader.py   # Utility functions for loading and converting data
│   └── app.py              # Main entry point for the Streamlit application
├── src-etl-microservice
│   ├── etl.py              # ETL logic for processing data
│   └── config.py           # Configuration settings for the ETL process
├── requirements.txt        # List of dependencies for the project
└── README.md               # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-microservice
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

4. Alternatively, you can use Docker to run the application:
   ```
   docker build -t airflightsfe:latest .
   docker run -p 8501:8501 -v ./shared-filesystem:/app/shared-filesystem airflightsfe:latest
   ```

## Usage Guidelines

- Navigate to the home page to get an overview of the application and its features.
- Use the explore page to visualize and understand the dataset.
- Access the analyze page to perform various analyses on the data.