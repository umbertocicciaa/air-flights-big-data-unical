#!/bin/bash

# Start Redis service
echo "Starting Redis service..."
redis-server --daemonize yes

# Clear Redis cache
echo "Clearing Redis cache..."
redis-cli FLUSHALL

# Set environment variables from a file
ENV_FILE="./src/local.env"
if [ -f $ENV_FILE ]; then
    export $(grep -v '^#' $ENV_FILE | xargs)
    echo "Environment variables loaded from $ENV_FILE file."
else
    echo "$ENV_FILE file not found. Skipping environment variable loading."
fi


# Start Streamlit app
echo "Starting Streamlit app..."
streamlit run src/home.py