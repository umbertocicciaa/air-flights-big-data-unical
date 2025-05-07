# Air flights big data unical

[![Airflights](https://github.com/umbertocicciaa/air-flights-big-data-unical/actions/workflows/airflights.yml/badge.svg)](https://github.com/umbertocicciaa/air-flights-big-data-unical/actions/workflows/airflights.yml)

## Project Overview

This project is designed to analyze and visualize air flight data using big data technologies. It includes data processing, storage, and visualization components to provide insights into various aspects of air travel.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.x
- Docker
- Docker Compose

## Installation

Clone the repository:

```sh
git clone https://github.com/umbertocicciaa/air-flights-big-data-unical.git
cd air-flights-big-data-unical
```

## Usage in local

To run the project locally:

```sh
set -a
source src/$ENV.env
set +a
python3 src/run.py
```

## Usage with docker compose

To run the project locally, use Docker Compose:

```sh
docker compose up
```
<!--
## Local installation hadoop and spark

Utilies urls.
<https://medium.com/@MinatoNamikaze02/installing-hadoop-on-macos-m1-m2-2023-d963abeab38e>
<https://medium.com/@le.oasis/setting-up-apache-spark-on-macos-a-comprehensive-guide-78af7642deb1>
-->
