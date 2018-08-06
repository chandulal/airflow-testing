import unittest
from datetime import datetime
from airflow import DAG
from airflow.models import TaskInstance
from airflow.operators import HelloWorldOperator


class TestMyHelloWorldOperator(unittest.TestCase):

    def test_execute(self):
        dag = DAG(dag_id='anydag', start_date=datetime.now())
        task = HelloWorldOperator(my_operator_param="This is for assertion", dag=dag, task_id='anytask')
        ti = TaskInstance(task=task, execution_date=datetime.now())
        result = task.execute(ti.get_template_context())
        self.assertEqual(result, "This is for assertion")


suite = unittest.TestLoader().loadTestsFromTestCase(TestMyHelloWorldOperator)
unittest.TextTestRunner(verbosity=2).run(suite)
