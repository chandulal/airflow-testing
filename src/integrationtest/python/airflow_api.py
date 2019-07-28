import requests
import json
import os


class AirflowAPI:
    def __init__(self):
        self.minikube_ip = self.get_minikube_ip()

    def get_minikube_ip(self):
        # minikube_ip = os.environ['MINIKUBE_IP']
        f = open("minikube_ip.txt", "r")
        minikube_ip = f.readlines()[0].replace('\n', '')
        if not minikube_ip:
            raise Exception("Minikube is not running. Please, start minikube first.")
        f.close()
        return minikube_ip

    def get_airflow_url(self):
        return "http://%s:%s" % (self.minikube_ip, 31317)

    def unpause_dag(self, dag_id):
        return requests.get(
            "%s/admin/rest_api/api?api=unpause&dag_id=%s" % (self.get_airflow_url(), dag_id))

    def pause_dag(self, dag_id):
        return requests.get(
            "%s/admin/rest_api/api?api=pause&dag_id=%s" % (self.get_airflow_url(), dag_id))

    def trigger_dag(self, dag_id, execution_date):
        self.clear_dag(dag_id, execution_date);
        self.unpause_dag(dag_id)
        triggered_response = requests.get(
            "%s/admin/rest_api/api?api=trigger_dag&dag_id=%s&exec_date=%s" % (
                self.get_airflow_url(), dag_id, execution_date))
        if triggered_response.status_code != 200:
            raise Exception("Please, wait for airflow web server to start.")

    def dag_state(self, dag_id, execution_date):
        return requests.get(
            "%s/admin/rest_api/api?api=dag_state&dag_id=%s&execution_date=%s" % (
                self.get_airflow_url(), dag_id, execution_date))

    def clear_dag(self, dag_id, execution_date):
        return requests.get(
            "%s/admin/rest_api/api?api=clear&dag_id=%s&execution_date=%s" % (
                self.get_airflow_url(), dag_id, execution_date))

    def is_dag_running(self, dag_id, execution_date):
        response = self.dag_state(dag_id, execution_date)
        json_response = json.loads(response.text)
        print(json_response)
        if "running" in json_response['output']['stdout']:
            return True
        else:
            self.pause_dag(dag_id)
            return False

    def get_dag_status(self, dag_id, execution_date):
        response = self.dag_state(dag_id, execution_date)
        json_response = json.loads(response.text)
        if "running" in json_response['output']['stdout']:
            return "running"
        elif "success" in json_response['output']['stdout']:
            return "success"
        elif "failed" in json_response['output']['stdout']:
            return "failed"
        else:
            return "Not Defined"

    def add_presto_connection(self, name, catalog, schema):
        conn_uri = "presto://" + self.minikube_ip + ":32211/" + catalog + "/" + schema
        return requests.get(
            "%s/admin/rest_api/api?api=connections&add=on&conn_id=%s&conn_uri=%s" % (
                self.get_airflow_url(), name, conn_uri))

    def add_mysql_connection(self, name, user, password, database):
        conn_uri = "mysql://" + user + ":" + password + "@" + self.minikube_ip + ":31320/" + database
        return requests.get(
            "%s/admin/rest_api/api?api=connections&add=on&conn_id=%s&conn_uri=%s" % (
                self.get_airflow_url(), name, conn_uri))
