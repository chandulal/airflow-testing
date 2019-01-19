#!/usr/bin/env bash
minikube start --cpus 4 --memory 8192
kubectl apply -f airflow.kube.yaml
minikube mount src/main/python/:/data