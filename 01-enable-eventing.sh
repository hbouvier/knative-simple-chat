#!/bin/sh
kubectl create namespace tutorial
kubectl label namespace tutorial knative-eventing-injection=enabled
kubectl label namespace tutorial istio-injection=enabled
kubectl config set-context --current --namespace=tutorial
