from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor

dag = DAG('dependency_dag', description='DAG with sensor', schedule_interval='@once',
          start_date=datetime(2019, 12, 10))

sensor = ExternalTaskSensor(task_id='dag_sensor', 
                            external_dag_id = 'another_dag_id', 
                            external_task_id = None, 
                            dag=dag, mode = 'reschedule')

task = DummyOperator(task_id='some_task', retries=1, dag=dag)

task.set_upstream(sensor)