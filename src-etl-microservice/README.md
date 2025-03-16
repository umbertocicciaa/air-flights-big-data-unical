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
   docker build -t airflightsbe:latest .
   ```

2. Run the Docker container:

   **Pull Docker Images**:
      Ensure you have the latest Docker images for Spark and Spark Worker. You can pull them from Docker Hub or your preferred Docker registry.
      ```bash
         docker pull bitnami/spark:latest
         docker pull bitnami/spark-worker:latest
      ```

   **Run Spark Master Container**:
      Start the Spark Master container. This container will act as the master node for your Spark cluster.
      ```bash
         docker run -d --name spark-master -h spark-master -p 7077:7077 -p 8080:8080 bitnami/spark:latest
      ```

   **Run Spark Worker Containers**:
      Start one or more Spark Worker containers. These containers will connect to the Spark Master and act as worker nodes in your Spark cluster.
      ```bash
         docker run -d --name spark-worker-1 --link spark-master:spark-master -e SPARK_WORKER_CORES=2 -e SPARK_WORKER_MEMORY=2G bitnami/spark-worker:latest
         docker run -d --name spark-worker-2 --link spark-master:spark-master -e SPARK_WORKER_CORES=2 -e SPARK_WORKER_MEMORY=2G bitnami/spark-worker:latest
      ```

   **Run application**:
      ```
      docker run -p 5000:5000 -v ./shared-filesystem:/mnt/shared-filesystem/:rw airflightsbe:latest
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