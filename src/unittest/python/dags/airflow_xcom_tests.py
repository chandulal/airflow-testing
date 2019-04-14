import unittest
from datetime import datetime
from airflow.models import DagBag, settings,TaskInstance



class TestXComExamplesDag(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag()

    def test_accessing_xcom_data_in_print_xcom_value(self):
        dag_id = 'xcom_examples'
        dag = self.dagbag.get_dag(dag_id)
        push_configurations_to_xcom = dag.get_task('push_configurations_to_xcom')
        print_xcom_value = dag.get_task('print_xcom_value')

        edate = datetime.now()

        push_configurations_to_xcomti = TaskInstance(task=push_configurations_to_xcom, execution_date=edate)
        context = push_configurations_to_xcomti.get_template_context()
        push_configurations_to_xcom.execute(context)

        print_xcom_valueti = TaskInstance(task=print_xcom_value, execution_date=edate)

        result = print_xcom_valueti.xcom_pull(key="test_xcom")
        self.assertEqual(result, 'value')



    def test_accessing_xcom_value_in_templated_field(self):
        dag_id = 'xcom_examples'
        dag = self.dagbag.get_dag(dag_id)
        push_configurations_to_xcom = dag.get_task('push_configurations_to_xcom')
    

        edate = datetime.now()

        push_configurations_to_xcomti = TaskInstance(task=push_configurations_to_xcom, execution_date=edate)
        context = push_configurations_to_xcomti.get_template_context()
        push_configurations_to_xcom.execute(context)

        use_templated_xcom_value = dag.get_task('bash_operator')
        use_templated_xcom_valueti = TaskInstance(task=use_templated_xcom_value, execution_date=edate)
        context = use_templated_xcom_valueti.get_template_context()

        operators_templated_field='bash_command'

        rt = use_templated_xcom_value.render_template

        content=getattr(use_templated_xcom_value,operators_templated_field)

        bash_command = rt(operators_templated_field, content, context)
        

        self.assertEqual(bash_command, 'echo value')




suite = unittest.TestLoader().loadTestsFromTestCase(TestXComExamplesDag)
unittest.TextTestRunner(verbosity=2).run(suite)