# airflow-testing
Airflow unit tests, DAG integrity tests, Pipeline definition tests

How to run the tests?

For now, each test is test suit itself. You can run any test file available inside test directory using python command.


Run DAG Integrity Test (available inside airflow-testing/test/dags/) using this command:
	   <pre>
	   python dag_integrity_test.py
	   </pre>

Run Pipeline Definition Test (available inside airflow-testing/test/dags/) using this command:
	<pre>
	python helloworld_dag_test.py
	</pre>

Run Operator Test (available inside airflow-testing/test/plugins/) using this command:
	<pre>
	python multiplyby5_operator_test.py
	</pre>

Run Sensor Test (available inside airflow-testing/test/plugins/) using this command:
	<pre>
	python helloworld_sensor.py
	</pre>

