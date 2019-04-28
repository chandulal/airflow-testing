import sys
import unittest

sys.path.append('../')
from airflow_api import AirflowAPI


class TestHelloWorldDag(unittest.TestCase):
    """Integration test for Hello world DAG"""

    def setUp(self):
        self.airflow_api = AirflowAPI()

    def test_hello_world(self):
        """helloword dag should run successfully"""
        execution_date = "2019-01-11T12:00:00+00:00"
        dag_id = "hello_world"
        self.airflow_api.trigger_dag(dag_id, execution_date)
        is_running = True
        while is_running:
            is_running = self.airflow_api.is_dag_running(dag_id, execution_date)
        self.assertEqual(is_running, False)
        self.assertEqual(self.airflow_api.get_dag_status(dag_id, execution_date), "success")


if __name__ == '__main__':
    unittest.main()
