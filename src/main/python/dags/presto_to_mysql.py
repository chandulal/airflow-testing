from airflow.operators.presto_to_mysql import PrestoToMySqlTransfer
from datetime import datetime
from airflow import DAG

default_args = {
    'email': ['hello@world.com']
}

dag = DAG('presto_to_mysql', description='Presto to Mysql Transfer', default_args=default_args,
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

PrestoToMySqlTransfer(
    presto_conn_id='presto-conn',
    mysql_conn_id='mysql-conn',
    task_id='presto_to_mysql_transfer',
    sql="""
       SELECT name, count(*) as count
       FROM blackhole.default.region
       GROUP BY name
       """,
    mysql_table='mysql_region',
    mysql_preoperator='TRUNCATE TABLE mysql_region;',
    dag=dag)
