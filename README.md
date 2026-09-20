# ETL Pipeline for Stock Market Data Collection and Analysis

Automated ETL pipeline for financial market data - PySpark transformations,
Apache Airflow orchestration, PostgreSQL storage, Docker deployment.

## Overview

Pulls daily OHLCV data for 4 instruments (AAPL, NVDA, TSLA, BTC-USD) from
Yahoo Finance, runs it through PySpark window functions (7-day moving
average, data cleansing), and loads the results into PostgreSQL via JDBC.
Orchestrated with Apache Airflow on a weekday schedule with automatic
retries on failure (no manual intervention required).

## Architecture

![Architecture](./Demonstration%20(images)/Architecture.svg)

---

## Stack

| Layer          | Technology                              |
|----------------|-----------------------------------------|
| Ingestion      | Python 3.11, yfinance                   |
| Transformation | PySpark 4.0 — window functions, JDBC    |
| Storage        | PostgreSQL 13                           |
| Orchestration  | Apache Airflow 2.9.0                    |
| Infrastructure | Docker, Docker Compose                  |

## Project Structure

```
finance_etl/
├── dags/
│   └── finance_etl_dag.py     # Airflow DAG: extract >> transform
├── etl/
│   ├── Dockerfile
│   ├── extract.py             # Data ingestion via yfinance API
│   ├── transform.py           # PySpark: cleansing, MA_7 calculation, JDBC load
│   ├── requirements.txt
│   └── postgresql-42.7.5.jar  # JDBC driver
├── .env.example               # Environment variable template (no secrets)
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/VladislavDubinkin/ETL-Pipeline-for-Stock-Market-Data-Collection-and-Analysis.git
cd ETL-Pipeline-for-Stock-Market-Data-Collection-and-Analysis
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env: set POSTGRES_USER and POSTGRES_PASSWORD
```

### 3. Spin up all services

```bash
docker-compose up --build -d
```

### 4. Check that containers are up

```bash
docker-compose ps
```

Everything should show `running` or `healthy`.

### 5. Open the Airflow UI

```
http://localhost:8080
Username: admin
Password: admin
```

### 6. Trigger the pipeline

In the Airflow UI: find the `finance_etl` DAG -> flip the toggle on → click "Trigger DAG".

### 7. Check the data landed in PostgreSQL

```bash
docker exec finance_warehouse psql -U postgres -d finance_dw \
  -c "SELECT ticker, COUNT(*) AS rows, \
             MIN(\"Date\") AS from_date, \
             MAX(\"Date\") AS to_date \
      FROM fact_stocks \
      GROUP BY ticker;"
```

## DAG Structure

```
extract ──► transform
```

**extract** - pulls daily OHLCV data from Yahoo Finance for the 4 instruments
(AAPL, NVDA, TSLA, BTC-USD) and saves raw CSVs to `data/raw/`.

**transform** - reads the raw CSVs with PySpark, computes 7-day moving
averages via window functions, and loads everything into PostgreSQL via JDBC.

**Schedule:** weekdays at 06:00 UTC (`0 6 * * 1-5`).
Auto-restarts on task failure, so it doesn't need hand-holding.

## Output Schema

| Column | Type    | Description               |
|--------|---------|---------------------------|
| Date   | DATE    | Trading date              |
| ticker | VARCHAR | Instrument symbol         |
| Close  | NUMERIC | Daily closing price       |
| MA_7   | NUMERIC | 7-day moving average      |

## Screenshots

### Airflow DAG — successful run
> ![DAG](./Demonstration%20(images)/5264992369000520112.jpg)

### Data in PostgreSQL
> ![DAG](./Demonstration%20(images)/5265140974868960806.jpg)

### MA_7 for NVDA
> ![DAG](./Demonstration%20(images)/5265140974868960807.jpg)

## Known Limitations

- Runs as a daily batch job (that means no real-time streaming layer yet).
- Dataset covers 2024–2026 (Yahoo Finance historical data); for live trading
  data you'll need to configure an API key in `.env`.

---
