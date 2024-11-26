from dags.api_cb.src.domain.request_api import fetch_data_from_api
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import tempfile
import logging

def etl_api_cb(endpoint: str, payload: str, bucket_name: str, folder: str) -> None:
    
    df_data = fetch_data_from_api(endpoint, payload)

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = f"{tmp_dir}/{payload['busDt']}_{payload['storeId']}.csv"
        df_data.to_csv(file_path, index=False)

        gcs_file_path = f"{folder}/{payload['busDt']}/{payload['storeId']}.csv"

        hook = GCSHook(gcp_conn_id='google_conn_default')
        hook.upload(bucket_name=bucket_name, object_name=gcs_file_path, filename=file_path)

        logging.info(f"Upload concluido para gs://{bucket_name}/{gcs_file_path}")