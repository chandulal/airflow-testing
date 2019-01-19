import sys
import unittest

sys.path.append('../')
from utils import *


class TestHelloWorldDag(unittest.TestCase):
    """Integration test for Hello world DAG"""

    def setUp(self):
        self.minikube_ip = get_minikube_ip()

    def test_hello_world(self):
        """helloword dag should run successfully"""
        execution_date = "2019-01-11T12:00:00+00:00"
        dag_id = "hello_world"
        triggered_response = trigger_dag(dag_id, execution_date)
        if triggered_response.status_code == 200:
            is_running = True
            while is_running:
                is_running = is_dag_running(dag_id, execution_date)
            self.assertEqual(is_running, False)
