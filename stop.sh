#!/bin/bash

kubectl delete -f configmap.yaml -f deployment.yaml -f service.yaml -f daemonset.yaml -f cronjob.yaml

echo "Wait for pods to terminate..."

while kubectl get pods -l 'app in (hw-app,log-agent)' 2>/dev/null | grep -q .; do
    sleep 3
done
echo ""

echo "Stop completed!"
