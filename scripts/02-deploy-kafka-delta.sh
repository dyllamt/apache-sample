helm install delta-storage ../k8s/delta/ -f ../k8s/delta/values.yaml --namespace dev
helm install kafka-cluster ../k8s/kafka/ -f ../k8s/kafka/values.yaml --namespace dev