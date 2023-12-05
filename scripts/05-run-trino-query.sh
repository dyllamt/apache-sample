kubectl apply -f ../k8s/trino/trino-query.yaml -n dev
kubectl wait --for=condition=complete --timeout=60s job/trino-query-job -n dev