import airflow
from airflow import models
from airflow.operators.postgres_to_gcs import PostgresToGoogleCloudStorageOperator


default_args = {"start_date": airflow.utils.dates.days_ago(1)}


GCS_BUCKET = "postgres_to_gcs_example"
FILENAME = "test_file"
QUERY = "select * from test_table;"


with models.DAG(
    dag_id='example_postgres_to_gcs',
    default_args=default_args,
    schedule_interval=None,  # Override to match your needs

) as dag:
    upload_data = PostgresToGoogleCloudStorageOperator(
        task_id="get_data",
        sql=QUERY,
        bucket=GCS_BUCKET,
        filename=FILENAME,
        gzip=False
    )