import unittest
from datetime import datetime
from airflow.models import DagBag, TaskInstance


class TestXComExamplesDag(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag()

    def test_xcoms(self):
        dag_id = 'hello_world_xcoms'
        dag = self.dagbag.get_dag(dag_id)
        push_to_xcoms_task = dag.get_task('push_to_xcoms')
        pull_from_xcoms_task = dag.get_task('pull_from_xcoms')

        execution_date = datetime.now()

        push_to_xcoms_ti = TaskInstance(task=push_to_xcoms_task, execution_date=execution_date)
        context = push_to_xcoms_ti.get_template_context()
        push_to_xcoms_task.execute(context)

        pull_from_xcoms_ti = TaskInstance(task=pull_from_xcoms_task, execution_date=execution_date)

        result = pull_from_xcoms_ti.xcom_pull(key="dummyKey")
        self.assertEqual(result, 'dummyValue')

    def test_xcom_in_templated_field(self):
        dag_id = 'hello_world_xcoms'
        dag = self.dagbag.get_dag(dag_id)
        push_to_xcoms_task = dag.get_task('push_to_xcoms')

        execution_date = datetime.now()

        push_to_xcoms_ti = TaskInstance(task=push_to_xcoms_task, execution_date=execution_date)
        context = push_to_xcoms_ti.get_template_context()
        push_to_xcoms_task.execute(context)

        templated_xcoms_value_task = dag.get_task('templated_xcoms_value')
        templated_xcoms_value_ti = TaskInstance(task=templated_xcoms_value_task, execution_date=execution_date)
        context = templated_xcoms_value_ti.get_template_context()

        bash_operator_templated_field = 'bash_command'

        rendered_template = templated_xcoms_value_task.render_template

        bash_command_value = getattr(templated_xcoms_value_task, bash_operator_templated_field)

        bash_command_rendered_value = rendered_template(bash_operator_templated_field, bash_command_value, context)

        self.assertEqual(bash_command_rendered_value, 'echo dummyValue')


suite = unittest.TestLoader().loadTestsFromTestCase(TestXComExamplesDag)
unittest.TextTestRunner(verbosity=2).run(suite)
