from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator


def associate_date_to_operator(operator_id: str):
    return f"{operator_id} - {datetime.now()}"


def _task_two(task):
    task_id = str(task.xcom_pull(task_ids=[f'operator_{operator_id}' for operator_id in ['one', 'two', 'three']]))
    task_id = task_id.split('-')[0].replace(' ', '')

    if task_id == 'two':
        return 'TWO'

    return 'NOT_TWO'


with DAG(dag_id="DAGIDAG", start_date=datetime(year=2023, month=5, day=27), schedule_interval='@daily',
         catchup=False) as dag:
    running_tasks = [PythonOperator(task_id=f"operator_{operator_id}", python_callable=associate_date_to_operator,
                                    op_kwargs={
                                        "operator_id": operator_id
                                    })
                     for operator_id in ['one', 'two', 'three']]

    correct_task = BranchPythonOperator(task_id="correct_task_finder", python_callable=_task_two)

    two = BashOperator(task_id="TWO", bash_command="echo 'Two is reached !' ")

    not_two = BashOperator(task_id="NOT_TWO", bash_command="echo 'Not two' ")

    running_tasks >> correct_task >> [two, not_two]
