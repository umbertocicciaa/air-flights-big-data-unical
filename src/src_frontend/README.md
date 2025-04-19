# Streamlit Multipage

This project is a Streamlit multipage designed for exploring and analyzing data in Parquet format. It integrates with an ETL microservice to load and process data efficiently.

## Project Structure

```
src_frontend
├── src
│   ├── pages
│   │   ├── airport_analysis.py     # Home page with introduction and navigation
│   │   ├── analyze.py              # Page for exploring data in Parquet format
│   │   ├── annual_analysis.py      # Page for performing data analysis
│   │   ├── classification.py
│   │   ├── clustering.py
│   │   ├── correlation.py
│   │   ├── dispersion.py
│   │   ├── explore.py
│   │   ├── fligth_finder.py
│   │   └── mounth_analysis.py
│   └── home.py                     # Main entry point for the Streamlit application
├── requirements.txt                # List of dependencies for the project
└── README.md                       # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd src/src_frontend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run src/home.py
   ```

## Usage Guidelines

- Navigate to the home page to get an overview of the application and its features.
- Use the explore page to visualize and understand the dataset.
- Access the analyze page to perform various analyses on the data.