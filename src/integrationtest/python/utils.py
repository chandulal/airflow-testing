import requests
import json
import subprocess


def get_minikube_ip():
    process = subprocess.Popen(["minikube", "ip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    if process.stdout is not None:
        minikube_ip = process.stdout.readline().strip()
        return "http://%s:%s" % (minikube_ip, 31317)
    raise Exception("Minikube is not running.")


def unpause_dag(dag_id):
    return requests.get(
        "%s/admin/rest_api/api?api=unpause&dag_id=%s" % (get_minikube_ip(), dag_id))


def pause_dag(dag_id):
    return requests.get(
        "%s/admin/rest_api/api?api=pause&dag_id=%s" % (get_minikube_ip(), dag_id))


def trigger_dag(dag_id, execution_date):
    unpause_dag(dag_id)
    return requests.get(
        "%s/admin/rest_api/api?api=trigger_dag&dag_id=%s&exec_date=%s" % (
            get_minikube_ip(), dag_id, execution_date))


def dag_state(dag_id, execution_date):
    return requests.get(
        "%s/admin/rest_api/api?api=dag_state&dag_id=%s&execution_date=%s" % (
            get_minikube_ip(), dag_id, execution_date))


def is_dag_running(dag_id, execution_date):
    response = dag_state(dag_id, execution_date)
    json_response = json.loads(response.text)
    print(json_response)
    if "success" not in json_response['output']['stdout']:
        return True
    else:
        pause_dag(dag_id)
        return False
