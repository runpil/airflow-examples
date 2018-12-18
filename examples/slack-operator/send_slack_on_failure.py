from airflow import models
from airflow.hooks.base_hook import BaseHook
import slack_operator # Only for airflow 1.9.0, this feature created in airflow 2.0.0
from airflow.operators.bash_operator import BashOperator


# You must setting slack connection
SLACK_CONN_ID = 'slack'


def task_fail_slack_alert(context):
    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
    slack_msg = """
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
        )
    failed_alert = slack_operator.SlackWebhookOperator(
        task_id='slack_test',
        http_conn_id='slack',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow',
        dag=dag)
    return failed_alert.execute(context=context)


default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2018, 12, 13), 
    'email': ['zzsza@naver.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


with models.DAG(
        dag_id='dag_id',
        description='Description',
        schedule_interval='1 0 * * *',  # Korea time 09:01 start
        default_args=default_args) as dag:

    bash_task = BashOperator(
        dag=dag,
        task_id='bash',
        bash_command='aaaaaa',
        on_failure_callback=task_fail_slack_alert
    )

    bash_task
