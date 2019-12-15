import airflow
from airflow.exceptions import AirflowSkipException
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}


# Create some placeholder operators
class DummySkipOperator(DummyOperator):
    """Dummy operator which always skips the task."""

    ui_color = '#e8b7e4'

    def execute(self, context):
        raise AirflowSkipException


def create_test_pipeline(suffix, trigger_rule, dag_):
    """
    Instantiate a number of operators for the given DAG.
    :param str suffix: Suffix to append to the operator task_ids
    :param str trigger_rule: TriggerRule for the join task
    :param DAG dag_: The DAG to run the operators on
    """
    skip_operator = DummySkipOperator(task_id='skip_operator_{}'.format(suffix), dag=dag_)
    always_true = DummyOperator(task_id='always_true_{}'.format(suffix), dag=dag_)
    join = DummyOperator(task_id=trigger_rule, dag=dag_, trigger_rule=trigger_rule)
    final = DummyOperator(task_id='final_{}'.format(suffix), dag=dag_)

    skip_operator >> join
    always_true >> join
    join >> final


dag = DAG(dag_id='example_skip_dag', default_args=args)
create_test_pipeline('1', 'all_success', dag)
create_test_pipeline('2', 'one_success', dag)