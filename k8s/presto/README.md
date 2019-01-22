Actual Source: https://github.com/dharmeshkakadia/presto-kubernetes

Presto-Kubernetes
=================

Run [Presto](https://prestodb.io/) cluster on [Kubernetes](https://kubernetes.io/).

1. Clone this.

    ``
    git clone https://github.com/dharmeshkakadia/presto-kubernetes/ && cd presto-kubernetes
    ``

2. Start Coordinator.

    ```
    kubectl create -f coordinator-deployment.yaml 
    kubectl create -f presto-service.yaml
    ```

3. Start Workers

    ``
    kubectl create -f worker-deployment.yaml
    ``

4. Start using Presto. You can find out the address to connect using service URL. 

    ```
    kubectl get service presto

    NAME      TYPE       CLUSTER-IP   EXTERNAL-IP   PORT(S)          AGE
    presto    NodePort   10.0.0.251   <none>        8080:30126/TCP   20h
    ```

    If you are using minikube, you can find out the address as follows

    ```
    minikube service presto --url
    
    http://192.168.64.4:30126
    ```

    Here is how you can use [presto-cli](https://prestodb.io/docs/current/installation/cli.html) to connect and start running queries. The presto UI is also available at the above URI. 

    ``
    presto-cli --server http://192.168.64.4:30126 --catalog tpch --schema sf1
    ``
