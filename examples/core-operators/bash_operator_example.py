from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2018, 12, 1),
    'email': ['your@maile.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('bash_dag', default_args=default_args, schedule_interval='@once'))

task1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

task2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=2,
    dag=dag)

task3 = BashOperator(
    task_id='pwd',
    bash_command='pwd',
    dag=dag)


task1 >> task2
task1 >> task3
