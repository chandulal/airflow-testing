import sys
import unittest

sys.path.append('../')
from airflow_api import AirflowAPI


class TestPrestoToMySqlDag(unittest.TestCase):
    """Integration test for presto to mysql transfer"""

    def setUp(self):
        self.airflow_api = AirflowAPI()
        self.airflow_api.add_presto_connection("presto-conn", "tpch", "sf1")
        self.airflow_api.add_mysql_connection("mysql-conn", "mysql", "mysql", "mysql")

    def test_presto_to_mysql_transfer(self):
        """should transfer data from presto to mysql"""
        execution_date = "2019-01-12T12:00:00+00:00"
        dag_id = "presto_to_mysql"
        self.airflow_api.trigger_dag(dag_id, execution_date)
        is_running = True
        while is_running:
            is_running = self.airflow_api.is_dag_running(dag_id, execution_date)
        self.assertEqual(is_running, False)
        self.assertEqual(self.airflow_api.get_dag_status(dag_id, execution_date), "success")
