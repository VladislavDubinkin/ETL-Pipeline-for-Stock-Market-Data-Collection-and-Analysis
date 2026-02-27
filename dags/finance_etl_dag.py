from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="finance_etl",
    default_args=default_args,
    description="ETL pipeline: extract → transform → PostgreSQL",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 6 * * 1-5",
    catchup=False,
    tags=["finance", "etl", "pyspark"],
) as dag:

    extract = BashOperator(
    task_id="extract",
    bash_command="docker exec finance_etl python /app/extract.py",
    )

    transform = BashOperator(
    task_id="transform",
    bash_command="docker exec finance_etl python /app/transform.py",
    )

    extract >> transform
