from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator


default_args = {
    'owner': 'kyle',
    'depends_on_past': False,
    'start_date': datetime(2018, 12, 1),
    'email': ['zzsza@naver.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(dag_id='gcs_to_bigquery',
          description='Google Cloud Storage to BigQuery!',
          schedule_interval='@daily', # For daily job(= 0 0 * * *)
          default_args=default_args)


task1 = GoogleCloudStorageToBigQueryOperator(
    dag=dag,
    task_id='1',
    schema_object='your_schema_file.json', # schema of you source data (in airflow 2.0 will add autodetect feature)
    bucket='BUCKET_NAME',
    source_objects=["your_source_file.csv"],
    source_format='CSV',
    destination_project_dataset_table='[PROJECT_NAME].[DATASET].[TABLE]', # ex : 'my-project.dataset.test
    write_disposition='WRITE_TRUNCATE',
    google_cloud_storage_conn_id='google_cloud_default' # you will set google cloud storage conn id in airflow web ui
)


task1
