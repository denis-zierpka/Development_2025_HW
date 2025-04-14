#!/bin/bash

if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "ERROR: Failed to connect to kubernetes cluster"
    echo "Check minikube status"
    exit 1
fi

echo "Apply configurations..."
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f daemonset.yaml
kubectl apply -f cronjob.yaml

echo "Wait for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=hw-app --timeout=60s
kubectl wait --for=condition=ready pod -l app=log-agent --timeout=60s

echo ""
echo "--- Deployment status: ---"
kubectl get deployments
echo ""
echo "--- Pods status: ---"
kubectl get pods
echo ""
echo "--- Services status: ---"
kubectl get services
echo ""
echo "--- DaemonSets status: ---"
kubectl get daemonsets
echo ""
echo "--- CronJobs status: ---"
kubectl get cronjobs
echo ""

echo "Deployment completed!"
