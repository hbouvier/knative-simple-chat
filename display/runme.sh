#!/bin/sh
kubectl create namespace tutorial
kubectl config set-context --current --namespace=tutorial
kubectl apply -f service.yaml 
