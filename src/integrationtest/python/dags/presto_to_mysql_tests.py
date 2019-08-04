import sys
import unittest
import mysql.connector
import prestodb

sys.path.append('../')
from airflow_api import AirflowAPI
from db_util import DBUtil
from constants import PRESTO_DB_PORT,MYSQL_DB_PORT


class TestPrestoToMySqlDag(unittest.TestCase):
    """Integration test for presto to mysql transfer"""

    mysql_conn = None
    prest_conn = None


    def setUp(self):
        presto_catlog="blackhole"
        presto_schema= "default"
        mysql_database="mysql"
        mysql_user="mysql"
        mysql_password="mysql"

        self.airflow_api = AirflowAPI()
        self.minikube_ip = str(self.airflow_api.get_minikube_ip())
        self.db_util = DBUtil()
        self.airflow_api.add_presto_connection("presto-conn",presto_catlog
                                               ,presto_schema)
        self.airflow_api.add_mysql_connection("mysql-conn", mysql_database,
                                              mysql_user, mysql_password)
        self.mysql_conn = mysql.connector.connect(user=mysql_user,
                                                  password=mysql_password,
                                                  host=self.minikube_ip,
                                                  port=MYSQL_DB_PORT,
                                                  database=mysql_database,
                                                  use_pure=False)

        self.prest_conn = prestodb.dbapi.connect(
            host=self.minikube_ip,
            port=PRESTO_DB_PORT,
            user='admin',
            catalog=presto_catlog,
            schema=presto_schema,
        )

        create_mysql_table_sql = """
             CREATE TABLE IF NOT EXISTS mysql_region (
                 name VARCHAR(50),count int(10)
             );
             """

        self.db_util.create_table(self.mysql_conn,create_mysql_table_sql)

        create_presto_table_sql = """
           CREATE TABLE region (
             name varchar
           )
           WITH (
             split_count = 1,
             pages_per_split = 1,
             rows_per_page = 1,
             page_processing_delay = '5s'
           )"""


        self.db_util.create_table(self.prest_conn,create_presto_table_sql)

        insert_query_1 =  "insert into region values('INDIA')"
        self.db_util.insert_into_table(self.prest_conn,insert_query_1)

    def test_presto_to_mysql_transfer(self):
        """should transfer data from presto to mysql"""

        execution_date = "2019-05-12T14:00:00+00:00"
        dag_id = "presto_to_mysql"
        self.airflow_api.trigger_dag(dag_id, execution_date)
        is_running = True
        while is_running:
            is_running = self.airflow_api.is_dag_running(dag_id, execution_date)
        self.assertEqual(is_running, False)
        self.assertEqual(self.airflow_api.get_dag_status(dag_id,
                                                         execution_date), "success")

        mysql_select_query = "SELECT name FROM mysql_region"
        row_count=self.db_util.get_row_count(self.mysql_conn,mysql_select_query)
        self.assertEqual(1, len(row_count))

    def tearDown(self):
        drop_mysql_table="drop table mysql_region"
        drop_presto_table = "drop table region"
        self.db_util.drop_table(self.mysql_conn,drop_mysql_table)
        self.db_util.drop_table(self.prest_conn,drop_presto_table)
        self.mysql_conn.close()
        self.prest_conn.close()


if __name__ == '__main__':
    unittest.main()
