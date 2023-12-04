kubectl apply -f trino/trino-catalogs.yaml -n dev
kubectl apply -f trino/trino-engine.yaml -n dev
kubectl apply -f trino/trino-init.yaml -n dev