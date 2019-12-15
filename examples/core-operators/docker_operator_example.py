import airflow
from airflow import DAG
from airflow.operators import BashOperator
from datetime import timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'docker_sample', default_args=default_args, schedule_interval=timedelta(minutes=10))

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

t3 = DockerOperator(api_version='1.19',
    docker_url='tcp://localhost:2375', #Set your docker URL
    command='/bin/sleep 30',
    image='centos:latest',
    network_mode='bridge',
    task_id='docker_op_tester',
    dag=dag)

t4 = BashOperator(
    task_id='print_hello',
    bash_command='echo "hello world!!!"',
    dag=dag)

t1 >> t2
t1 >> t3
t3 >> t4
