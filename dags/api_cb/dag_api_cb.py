from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from api_cb.src.domain.config import endpoints, payload, BUCKET_NAME, FOLDER_BASE
from api_cb.src.domain.main import etl_api_cb
import pendulum
from datetime import timedelta


default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='api_cb_data_lake',
    default_args=default_args,
    schedule_interval=None,
    start_date=pendulum.datetime(2024, 1, 1),
    catchup=False
) as dag:
    
    start = EmptyOperator(
        task_id='start'
    )

    endpoint_tasks = []
    for endpoint in endpoints:
        endpoint_task = PythonOperator(
            task_id=f"etl_{endpoint.split('/')[-1]}",
            python_callable=etl_api_cb,
            op_kwargs={
                "endpoint": endpoint,
                "payload": payload,
                "bucket_name": BUCKET_NAME,
                "folder": f"{FOLDER_BASE}/{endpoint.split('/')[-1]}"
            }
        )
        endpoint_tasks.append(endpoint_task)

    end = EmptyOperator(
        task_id='end'
    )

start >> endpoint_tasks >> end