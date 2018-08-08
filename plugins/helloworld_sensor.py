from datetime import datetime, timedelta
import time
import logging
from airflow.operators.sensors import BaseSensorOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults

log = logging.getLogger(__name__)

class HelloworldSensor(BaseSensorOperator):

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(HelloworldSensor, self).__init__(*args, **kwargs)
    
    def poke(self, context):
        current_minute = self.params.get('sensor_start_time').minute
        if current_minute % 3 != 0:
            log.info("Sensor minute (%s) is not divisible by 3, sensor will retry.", current_minute)
            self.params['sensor_start_time'] = self.params.get('sensor_start_time') + timedelta(minutes=1)
            return False

        log.info("Sensor minute (%s) is divisible by 3, sensor finished.", current_minute)
        return True

    def execute(self, context):
        self.params['poke_count'] = 0
        while not self.poke(context):
            self.params['poke_count'] = self.params.get('poke_count') + 1
            time.sleep(self.poke_interval)
        return self.params.get('poke_count')


class HelloworldSensorPlugin(AirflowPlugin):
    name = "helloworld_sensor_plugin"
    operators = [HelloworldSensor]

def get_now():
    return datetime.now()
