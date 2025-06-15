#!/bin/bash

NAMESPACE="airfligth"

if [ "$1" == "install" ]; then
    kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    kubectl apply -f k8s/ -n $NAMESPACE
    # kubectl port-forward service/frontend 8501:8501 -n $NAMESPACE
else
    kubectl delete -f k8s/ -n $NAMESPACE
    kubectl delete namespace $NAMESPACE
fi