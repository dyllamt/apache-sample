helm repo add apache-airflow https://airflow.apache.org
helm repo update
export NAMESPACE=airflow
kubectl create namespace $NAMESPACE
export RELEASE_NAME=airflow
helm upgrade $RELEASE_NAME apache-airflow/airflow --namespace $NAMESPACE \
    --set images.airflow.repository=my-image \
    --set images.airflow.tag=0.0.1
kubectl port-forward svc/$RELEASE_NAME-webserver 8080:8080 --namespace $NAMESPACE