from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from erp_cb.src.domain.main import *
import pendulum

JSON_FILE_PATH = "/opt/airflow_docker/dags/src/domain/ERP.json"
POSTGRES_CONN_ID = "postgres_conn_default"
default_args = {"owner": "airflow", "retries": 1}


with DAG(
    dag_id="erp_cb",
    start_date=pendulum.datetime(2024, 1, 1, tz="America/Sao_Paulo"),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    tags=["erp"],
) as dag:

    start = EmptyOperator(task_id="start")

    create_tables_task = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="/opt/airflow_docker/dags/sql/create_tables.sql",
    )

    etl_erp_cb_task = PythonOperator(
        task_id="extract_json",
        python_callable=etl_erp_cb,
        op_kwargs={
            'file_path': JSON_FILE_PATH, 
            'postgres_conn': POSTGRES_CONN_ID
        }
    )

    end = EmptyOperator(task_id='end')

start >> create_tables_task >> etl_erp_cb_task >> end
