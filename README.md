# ✈️ Air Flights Big Data @ Unical

[![CI - Airflights](https://github.com/umbertocicciaa/air-flights-big-data-unical/actions/workflows/airflights.yml/badge.svg)](https://github.com/umbertocicciaa/air-flights-big-data-unical/actions/workflows/airflights.yml)

Analyze and visualize air traffic data at scale using a modern big data stack. This project demonstrates distributed processing with Hadoop and Spark, real-time analytics with Redis, and containerized orchestration via Docker.

---

## 📊 Demo

![Demo](resources/demo.png)

---

## 🚀 Features

- Distributed data processing with **Apache Spark**
- HDFS storage via **Hadoop**
- Data warehouse storage via **Hive**
- In-memory caching and messaging using **Redis**
- Scalable and isolated setup via **Docker Compose** or **K8S**

---

## 🧱 Project Structure

```
air-flights-big-data-unical/
├── src/                    # Application code and environment settings
├── run.sh                  # Script for local (non-Docker) execution
├── docker-compose.yml      # Multi-service Docker configuration (DEV)
├── docker-compose-prod.yml # Multi-service Docker configuration (PROD)
├── src/Dockerfile          # Base image for application container
└── resources/              # Static assets and demo images
```

---

## ☸️ Run with K8s

### Prerequisites

- Kubernetes Cluster
- [kubectl](https://kubernetes.io/docs/reference/kubectl/)
- Dataset provided by the instructor

### Usage

This will spin up all required services (Hadoop, Hive, Spark, Redis, App) automatically.

```bash
chmod u+x install_cluster.sh
./install_cluster.sh install
```

Withot install input you destroy the namespace

```bash
chmod u+x install_cluster.sh
./install_cluster.sh
```

---

## 🐳 Run with Docker Compose

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Dataset provided by the instructor

### Usage

```bash
docker compose -f docker-compose-prod.yaml
```

This will spin up all required services (Hadoop, Spark, Redis, App) automatically.

---

## 💻 Run Locally (Manual Setup)

### Prerequisites

- Python 3.x
- Redis
- Apache Spark
- Apache Hadoop
- Java JDK (8 or 11)
- Dataset provided by the instructor

### Steps

```bash
# Set JAVA_HOME in src/local.env to your JDK 8 or 11 path
# Example: 
JAVA_HOME=/usr/lib/jvm/java-11-openjdk

# Make script executable and run
chmod u+x run_local.sh
./run_local.sh
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---
