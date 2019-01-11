import glob

import yaml
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def extract(**kwargs):
    print(kwargs)


def transform(**kwargs):
    print (kwargs)


def load(**kwargs):
    print(kwargs)


os.chdir(os.environ['AIRFLOW_HOME'] + "/dags/mysql-ingestion/")

for y in glob.glob('*.yaml'):
    print(y)
    with open(y, 'r') as f:
        dag_meta = yaml.safe_load(f)
    dag = DAG(dag_id=dag_meta['dag_id'], start_date=dag_meta['start_date'])

    task_bag = {}
    pattern = dag_meta['pattern']

    for e in pattern['extract']:
        task_id = 'extract{}'.format(e['source'])
        task = PythonOperator(task_id=task_id, python_callable=extract, op_kwargs=e, dag=dag)
        task_bag[task_id] = task

    for t in pattern['transform']:
        task_id = 'transform{}'.format(t['transform'])
        task = PythonOperator(task_id=task_id, python_callable=transform, op_kwargs=t, dag=dag)

        task.set_upstream(task_bag['extract{}'.format(t['transform'])])
        task_bag[task_id] = task

    for l in pattern['load']:
        task_id = 'load{}'.format(l['sink'])
        task = PythonOperator(task_id=task_id, python_callable=load, op_kwargs=l, dag=dag)

        task.set_upstream(task_bag['transform{}'.format(l['sink'])])
        task_bag[task_id] = task

    globals()[dag_meta['dag_id']] = dag
