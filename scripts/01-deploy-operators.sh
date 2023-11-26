#!/bin/bash

kubectl create namespace dev

# strimzi operator
helm repo add strimzi http://strimzi.io/charts/
helm repo update
helm install strimzi-operator strimzi/strimzi-kafka-operator --namespace dev

# spark operator
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm repo update
helm install spark-operator spark-operator/spark-operator --namespace dev --set sparkJobNamespace=dev --set webhook.enable=true