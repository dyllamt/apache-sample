
# delta storage on local file system with hive metastore
helm install delta-storage ../k8s/delta/ -f ../k8s/delta/values.yaml --namespace dev --wait
kubectl wait --for=condition=available deployment.apps/hive-standalone -n dev


# trino engine referencing delta warehouse and hive metastore
kubectl apply -f ../k8s/trino/trino-catalogs.yaml -n dev
kubectl apply -f ../k8s/trino/trino-engine.yaml -n dev
kubectl wait --for=condition=available deployment.apps/trino -n dev
kubectl apply -f ../k8s/trino/trino-init.yaml -n dev