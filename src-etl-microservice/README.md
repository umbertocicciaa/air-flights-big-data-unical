# REST API for CSV to Parquet Conversion

This project provides a REST API that allows users to upload a CSV file and receive a Parquet version of the file with selected columns.

## Project Structure

```
rest-api-project
├── src
│   ├── app.py          # Entry point for the Flask application
│   ├── etl.py          # ETL process for converting CSV to Parquet
│   └── utils
│       └── __init__.py # Utility functions and constants
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Requirements

To run this project, you need to have Python installed along with the following packages:

- Flask
- PySpark

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Running the API

1. Navigate to the project directory:

   ```
   cd rest-api-project
   ```

2. Start the Flask application:

   ```
   python src/app.py
   ```

3. The API will be available at `http://127.0.0.1:5000`.

## API Endpoint

### Upload CSV

- **Endpoint:** `/upload`
- **Method:** `POST`
- **Description:** Upload a CSV file to convert it to Parquet format.
- **Request:**
  - Form-data with a file field named `file` containing the CSV file.
  
- **Response:**
  - Returns the Parquet file as a response.

## Example Usage

You can use tools like `curl` or Postman to test the API. Here’s an example using `curl`:

```
curl -X POST -F "file=@path/to/your/file.csv" http://127.0.0.1:5000/upload
```

This will return the Parquet file in response.