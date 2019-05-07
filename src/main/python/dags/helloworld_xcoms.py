import datetime
from airflow import DAG
from airflow.operators import PythonOperator
from airflow.operators import BashOperator

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    'start_date': yesterday,
    'email_on_failure': False,
    'email_on_retry': False,
    'email': ['hello@world.com'],
    'retries': 0
}


def push_to_xcoms(*args, **kwargs):
    value = "dummyValue"
    kwargs['ti'].xcom_push(key="dummyKey", value=value)


def pull_from_xcoms(**kwargs):
    ti = kwargs['ti']
    pulled_value = ti.xcom_pull(key='dummyKey', task_ids='push_to_xcoms')
    print("value=" + str(pulled_value))


dag = DAG('hello_world_xcoms', description='Hello world XComs example', default_args=default_dag_args, schedule_interval=None)

push_to_xcoms_task = PythonOperator(
    task_id='push_to_xcoms',
    provide_context=True,
    python_callable=push_to_xcoms,
    dag=dag
)

pull_from_xcoms_task = PythonOperator(
    task_id='pull_from_xcoms',
    provide_context=True,
    python_callable=pull_from_xcoms,
    dag=dag
)

templated_xcoms_value_task = BashOperator(
    task_id='templated_xcoms_value',
    bash_command='echo ' + str("{{ ti.xcom_pull(key='dummyKey')}}"),
    dag=dag
)

push_to_xcoms_task >> pull_from_xcoms_task >> templated_xcoms_value_task
