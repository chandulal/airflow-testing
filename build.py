from pybuilder.core import init,use_plugin

@init
def initialize(project):
    project.set_property("run_unit_tests_propagate_stdout", True)
    project.set_property("run_unit_tests_propagate_stderr", True)
    project.depends_on("apache-airflow", "==1.10.0")
    project.depends_on("cryptography", "==2.2.1")
    project.depends_on("requests", "==2.21.0")
    project.depends_on("mysqlclient", "==1.4.2")
    project.set_property('verbose', True)

use_plugin("exec")
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin('python.install_dependencies')
use_plugin('python.integrationtest')

default_task = ['clean']

