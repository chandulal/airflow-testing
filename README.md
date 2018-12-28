# airflow-testing
Airflow unit tests, DAG integrity tests and Pipeline definition tests

## Setup
Install Python 2.7.13 using pyenv:
<pre>
brew install pyenv
pyenv install 2.7.13
pyenv global 2.7.13
pyenv global (Verify the python version)
</pre>

Install Pip and PyBuilder
<pre>
easy_install pip
pip install pybuilder
</pre>

Set AIRFLOW_HOME
<pre>
export AIRFLOW_HOME={project dir}/src/main/python
</pre>

Go to project root directory and run these commands:
<pre>
pyb install_dependencies
airflow initdb
pyb run_unit_tests
</pre>
