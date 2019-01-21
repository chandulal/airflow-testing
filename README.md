# Airflow Testing & Local/Dev Setup using Kubernetes

## Airflow Testing
Airflow unit tests, DAG integrity tests and Pipeline definition tests

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
</pre>

Please update $AIRFLOW_HOME/airflow.cfg:
<pre>
load_examples = False
</pre>

Run tests:
<pre>
pyb run_unit_tests
</pre>

## Airflow Local/Dev Setup using Kubernetes

Follow this steps to install and run airflow on dev machine. This will setup following components: <br />
   * Postgres (To store the metadata of airflow)
   * Redis (Broker for celery executors)
   * Airflow Scheduler
   * Celery Workers
   * Airflow Web Server
   * Flower

1) Install minikube
    <pre>
    brew cask install minikube
    brew install kubernetes-cli
    minikube start --cpus 4 --memory 8192
    </pre>
2) Mount DAGs,Plugins, etc. in minikube
    <pre> 
    minikube mount {project dir}/src/main/python/:/data
    </pre>
3) Go to project root dir and run:
    <pre> 
    kubectl apply -f airflow.kube.yaml
    </pre>
    wait for 3-4 min to start all airflow components.
4) Get Minikube ip:
    <pre>
    minikube ip
    </pre>
5) Now you can access: 

    **Airflow UI:** {minikube-ip}:31317 
    
    **Flower:** {minikube-ip}:32081

## How it works?

![minkube_airflow_architecture](https://github.com/chandulal/airflow-testing/blob/master/how_minikube_work.png)
