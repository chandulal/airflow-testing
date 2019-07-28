# Airflow Testing & Local/Dev Setup using Kubernetes

## Airflow Unit Testing

Go to project root directory and build the image
<pre>
docker build . -t airflow-test
</pre>

Run the unit tests from the docker. Use your repository location fo **{SourceDir}**
<pre>
docker run -ti  -v {SourceDir}/airflow-testing:/opt --entrypoint /mnt/entrypoint.sh airflow-test run_unit_tests
</pre>

## Airflow Local/Dev Setup using Kubernetes

Follow this steps to install and run airflow on dev machine. This will setup following components: <br />
   * Postgres (To store the metadata of airflow)
   * Redis (Broker for celery executors)
   * Airflow Scheduler
   * Celery Workers
   * Airflow Web Server
   * Flower
   
Prerequisite:
    <pre>
    git clone https://github.com/chandulal/airflow-testing.git
    brew cask install virtualbox (run if you don't have virtual box installed)
    </pre>

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
3) Open new terminal. Go to project root dir and run:
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
