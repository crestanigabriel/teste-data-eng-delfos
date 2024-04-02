# Teste Data Engineer - Delfos

Test instructions [here](./teste_data_eng.pdf).

## Table of Contents
- [Environment](#environment)
- [Setup instructions](#setup-instructions)
- [Source DB](#source-db)
- [Target DB](#target-db)
- [Source DB API](#source-db-api)
- [Links](#links)

## Environment
- **Python version**: 3.12.2
- **OS**: Windows 11, using WSL2 with Ubuntu 22.04.3

## Setup instructions
### Running docker compose (Source DB - postgresql, Target DB - postgresql, and Source DB API - FastAPI):
```bash
docker compose up
```
### Running ETL script:
To setup (from repo root folder):
```bash
cd etl_script
python -m venv env
source env/bin/activate
python instal -r requirements.txt
```
To run:
```bash
python main.py -d <date: yyyy-mm-dd>
```
Example:
```bash
python main.py -d "2023-01-10"
```

### Running Dagster
To setup (from repo root folder):
```bash
cd my_dagster
python -m venv env
source env/bin/activate
python instal -r requirements.txt
```
To run:
```bash
dagster dev
```

## Source DB
Table schema:

    - data
        - timestamp TIMESTAMP,
        - wind_speed DECIMAL,
        - power DECIMAL,
        - ambient_temperature DECIMAL,

        - PRIMARY KEY (timestamp)


Script used to generate data: **source_db/create_mock_data.sql**.  
This script generated data with **1-min interval**, between **2024-01-01 01:30:00** and **2024-01-11 01:29:00**.  
This data can be found in: **source_db/dataset/data.csv**.  

Exposed port to host: 5432

## Target DB
Tables schema:

    - signal
        - id INT,
        - name VARCHAR(20),
        - name VARCHAR(20),

        - PRIMARY KEY (id)

    - data
        - timestamp TIMESTAMP,
        - signal_id INT,
        - value DECIMAL,

        - PRIMARY KEY (timestamp, signal_id),
        - FOREIGN KEY (signal_id) REFERENCES signal(id)

Exposed port to host: 5433

## Source DB API
Exposed port to host: 8081  
Exposed endpoints:
- GET http://localhost:8081/health-check
- POST http://localhost:8081/data 

Example:

    Method: POST
    URL: http://localhost:8081/data
    Body:
        {
            "start_datetime": "2024-01-08T07:01:01",
            "end_datetime": "2024-01-08T08:01:01",
            "fields": ["wind_speed", "power"]
        }

## Links
Used references:

- [Dockerizing FastAPI with Postgres, Uvicorn](https://testdriven.io/blog/fastapi-docker-traefik/)
- [[OFICIAL DOC] FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Initializing a PostgreSQL Database with a Dataset using Docker Compose](https://medium.com/@asuarezaceves/initializing-a-postgresql-database-with-a-dataset-using-docker-compose-a-step-by-step-guide-3feebd5b1545)
- [[OFICIAL DOC] FastAPI with SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [[OFICIAL DOC] HTTPX Quickstart](https://www.python-httpx.org/quickstart/)
- [[OFICIAL DOC] Dagster](https://docs.dagster.io/getting-started)