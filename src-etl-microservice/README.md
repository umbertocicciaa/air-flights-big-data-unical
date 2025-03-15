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

To run this project, you need to have Docker installed.

## Running the API

0. Enter in the directory:
  
   ```
   cd src-etl-microservice
   ```

1. Build the Docker image:

   ```
   docker build -t rest-api-project .
   ```

2. Run the Docker container:

   ```
   docker run -p 5000:5000 rest-api-project
   ```

3. The API will be available at `http://localhost:5000`.

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
curl -X POST -F "file=@path/to/your/file.csv" http://localhost:5000/upload
```

This will return the Parquet file in response.