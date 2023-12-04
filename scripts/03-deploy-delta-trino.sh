
# delta storage on local file system with hive metastore
helm install delta-storage ../k8s/delta/ -f ../k8s/delta/values.yaml --namespace dev --wait

# trino engine referencing delta warehouse and hive metastore
kubectl apply -f trino/trino-catalogs.yaml -n dev
kubectl apply -f trino/trino-engine.yaml -n dev
kubectl apply -f trino/trino-init.yaml -n dev