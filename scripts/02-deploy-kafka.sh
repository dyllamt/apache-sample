#!/bin/bash

# Install Kafka cluster with Helm
helm install kafka-cluster ../k8s/kafka/ -f ../k8s/kafka/values.yaml --namespace dev --wait

# Wait for the Kafka pod to be created
POD_NAME="kafka-cluster-kafka-0"
NAMESPACE="dev"
echo "Waiting for pod $POD_NAME to be created..."
while : ; do
    kubectl get pod $POD_NAME -n $NAMESPACE &> /dev/null && break
    echo "Waiting for pod $POD_NAME to be created..."
    sleep 10
done

# Now wait for the pod to be ready
echo "Waiting for pod $POD_NAME to be ready..."
kubectl wait --for=condition=Ready pod/$POD_NAME -n $NAMESPACE --timeout=300s

echo "$POD_NAME is ready."
