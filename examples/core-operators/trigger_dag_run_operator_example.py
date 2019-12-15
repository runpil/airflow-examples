import airflow.utils.dates
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator

dag = DAG(
    dag_id="example_trigger_controller_dag",
    default_args={"owner": "airflow", "start_date": airflow.utils.dates.days_ago(2)},
    schedule_interval="@once",
)

trigger = TriggerDagRunOperator(
    task_id="test_trigger_dagrun",
    trigger_dag_id="example_trigger_target_dag",  # Ensure this equals the dag_id of the DAG to trigger
    conf={"message": "Hello World"},
    dag=dag,
)