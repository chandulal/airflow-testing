from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators import HelloWorldOperator

def print_hello():
 return 'Hello Wolrd'

dag = DAG('hello_world', description='Hello world example', schedule_interval='0 12 * * *', start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries = 3, dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

my_hello_operator = HelloWorldOperator(my_operator_param='my_operator_param',
                                task_id='my_helloworld_operator_task', dag=dag)

dummy_operator >> hello_operator

