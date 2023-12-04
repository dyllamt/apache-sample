# setup kafka cluster
helm install kafka-cluster ../k8s/kafka/ -f ../k8s/kafka/values.yaml --namespace dev --wait