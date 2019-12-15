import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

dag = DAG(
    dag_id="example_trigger_target_dag",
    default_args={"start_date": airflow.utils.dates.days_ago(2), "owner": "Airflow"},
    schedule_interval=None,
)


def run_this_func(**context):
    """
    Print the payload "message" passed to the DagRun conf attribute.
    :param context: The execution context
    :type context: dict
    """
    print("Remotely received value of {} for key=message".format(context["dag_run"].conf["message"]))


run_this = PythonOperator(task_id="run_this", python_callable=run_this_func, dag=dag)

bash_task = BashOperator(
    task_id="bash_task",
    bash_command='echo "Here is the message: \'{{ dag_run.conf["message"] if dag_run else "" }}\'"',
    dag=dag,
)