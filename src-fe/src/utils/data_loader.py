import pandas as pd


file_path = "shared-filesystem/outputs/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2013_3.csv/"
def load_parquet_data():
    try:
        data = pd.read_parquet(file_path)
        return data
    except Exception as e:
        print(f"Error loading Parquet file: {e}")
        return None

def convert_data_to_dataframe(data):
    if isinstance(data, pd.DataFrame):
        return data
    else:
        print("Provided data is not a valid DataFrame.")
        return None

def get_data_summary(data):
    if isinstance(data, pd.DataFrame):
        return data.describe()
    else:
        print("Provided data is not a valid DataFrame.")
        return None