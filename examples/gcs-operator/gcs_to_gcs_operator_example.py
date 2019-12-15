import os

import airflow
from airflow import models
from airflow.operators.gcs_to_gcs import GoogleCloudStorageSynchronizeBuckets

default_args = {"start_date": airflow.utils.dates.days_ago(1)}

BUCKET_1_SRC = os.environ.get("GCP_GCS_BUCKET_1_SRC", "test-gcs-sync-1-src")
BUCKET_1_DST = os.environ.get("GCP_GCS_BUCKET_1_DST", "test-gcs-sync-1-dst")

BUCKET_2_SRC = os.environ.get("GCP_GCS_BUCKET_2_SRC", "test-gcs-sync-2-src")
BUCKET_2_DST = os.environ.get("GCP_GCS_BUCKET_2_DST", "test-gcs-sync-2-dst")

BUCKET_3_SRC = os.environ.get("GCP_GCS_BUCKET_3_SRC", "test-gcs-sync-3-src")
BUCKET_3_DST = os.environ.get("GCP_GCS_BUCKET_3_DST", "test-gcs-sync-3-dst")


with models.DAG(
        "example_gcs_to_gcs", default_args=default_args, schedule_interval=@once
) as dag:
    sync_full_bucket = GoogleCloudStorageSynchronizeBuckets(
        task_id="sync-full-bucket",
        source_bucket=BUCKET_1_SRC,
        destination_bucket=BUCKET_1_DST
    )

    sync_to_subdirectory_and_delete_extra_files = GoogleCloudStorageSynchronizeBuckets(
        task_id="sync_to_subdirectory_and_delete_extra_files",
        source_bucket=BUCKET_1_SRC,
        destination_bucket=BUCKET_1_DST,
        destination_object="subdir/",
        delete_extra_files=True,
    )

    sync_from_subdirectory_and_allow_overwrite_and_non_recursive = GoogleCloudStorageSynchronizeBuckets(
        task_id="sync_from_subdirectory_and_allow_overwrite_and_non_recursive",
        source_bucket=BUCKET_1_SRC,
        source_object="subdir/",
        destination_bucket=BUCKET_1_DST,
        recursive=False,
    )

sync_full_bucket >> sync_to_subdirectory_and_delete_extra_files >> sync_from_subdirectory_and_allow_overwrite_and_non_recursive