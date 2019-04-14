import datetime
from airflow import models
from airflow.operators import PythonOperator
from airflow.operators import BashOperator
from airflow.utils import trigger_rule
from airflow.utils.decorators import apply_defaults


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


with models.DAG(
        'xcom_examples',
        schedule_interval=None,
        default_args=default_dag_args) as dag:

    def init_args(*args, **kwargs):
        testval="value"
        kwargs['ti'].xcom_push(key="test_xcom", value=testval)


    push_configurations_to_xcom = PythonOperator(
        task_id='push_configurations_to_xcom',
        provide_context=True,
        python_callable=init_args
    )


    def pull_xcom_data(**kwargs):
    	ti = kwargs['ti']

    	v3 = ti.xcom_pull(key='test_xcom',task_ids='push_configurations_to_xcom')
    	print("v3" + str(v3))


    print_xcom_value = PythonOperator(
        task_id='print_xcom_value',
        provide_context=True,
        python_callable=pull_xcom_data
    )


    use_templated_xcom_value= BashOperator(
        task_id = 'bash_operator',
        bash_command = 'echo '+ str("{{ ti.xcom_pull(key='test_xcom')}}")
    )

	
    push_configurations_to_xcom >> print_xcom_value >> use_templated_xcom_value
