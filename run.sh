#!/bin/bash

echo "Starting Redis service..."
redis-server --daemonize yes

echo "Clearing Redis cache..."
redis-cli FLUSHALL

ENV_FILE="./src/local.env"
if [ -f $ENV_FILE ]; then
    export $(grep -v '^#' $ENV_FILE | xargs)
    echo "Environment variables loaded from $ENV_FILE file."
else
    echo "$ENV_FILE file not found. Skipping environment variable loading."
fi

echo "Starting Streamlit app..."
streamlit run src/home.py