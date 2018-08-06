import logging

from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults

log = logging.getLogger(__name__)

class MyFirstOperator(BaseOperator):
   @apply_defaults
   def __init__(self, my_operator_param, *args, **kwargs):
     self.operator_param = my_operator_param
     super(MyFirstOperator, self).__init__(*args, **kwargs)
  
   def execute(self, context):
     log.info("hello world")
     log.info('operator_param: %s', self.operator_param)
     task_instance = context['task_instance']
     sensor_minute = task_instance.xcom_pull('my_sensor_task', key='sensor_minute')
     log.info('valid minute as determined by sensor: %s', sensor_minute)
     return 10

from datetime import datetime
from airflow.operators.sensors import BaseSensorOperator

class MyFirstSensor(BaseSensorOperator):
  @apply_defaults
  def __init__(self, *args, **kwargs):
   super(MyFirstSensor, self).__init__(*args, **kwargs)
 
  def poke(self, context):
   current_minute = datetime.now().minute
   if current_minute % 3 != 0:
    log.info("Current minute (%s) not is divisible by 3, sensor will retry.", current_minute)
    return False
   
   log.info("Current minute (%s) is divisible by 5, sensor finishing.", current_minute)
   task_instance = context['task_instance']
   task_instance.xcom_push('sensor_minute', current_minute)
   return True

class MyFirstPlugin(AirflowPlugin):
  name="my_first_plugin"
  operators = [MyFirstOperator, MyFirstSensor]
