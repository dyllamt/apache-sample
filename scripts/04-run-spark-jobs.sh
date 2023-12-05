# setup environmental variables for sources/sinks
kubectl apply -f ../k8s/spark/job-env-variables.yaml -n dev

# start structured streaming
kubectl apply -f ../k8s/spark/spark-application-ingest.yaml -n dev
NAMESPACE="dev"
APP_NAME="pyspark-ingest"
TIMEOUT=300  # Timeout in seconds
INTERVAL=10  # Check interval in seconds
elapsed=0
echo "Waiting for SparkApplication '$APP_NAME' to start running..."
while : ; do
    status=$(kubectl get sparkapplication $APP_NAME -n $NAMESPACE -o=jsonpath='{.status.applicationState.state}')
    if [[ $status == "RUNNING" ]]; then
        echo "Application is running."
        break
    fi
    if [[ $status == "FAILED" || $status == "COMPLETED" || $status == "UNKNOWN" ]]; then
        echo "Application is not in a running state. Current status: $status"
        exit 1
    fi
    if [[ $elapsed -ge $TIMEOUT ]]; then
        echo "Timed out waiting for the application to start."
        exit 1
    fi
    sleep $INTERVAL
    elapsed=$((elapsed + INTERVAL))
done

# produce sample data for streaming and wait for ingest to consume
kubectl apply -f ../k8s/spark/kafka-producer-job.yaml -n dev
kubectl wait --for=condition=complete --timeout=60s job/kafka-producer-job -n dev
sleep 30

# run aggregation job
kubectl apply -f ../k8s/spark/spark-application-aggregate.yaml -n dev
NAMESPACE="dev"
APP_NAME="pyspark-aggregate"
TIMEOUT=300  # Timeout in seconds
INTERVAL=10  # Check interval in seconds
elapsed=0
echo "Waiting for SparkApplication '$APP_NAME' to start finish..."
while : ; do
    status=$(kubectl get sparkapplication $APP_NAME -n $NAMESPACE -o=jsonpath='{.status.applicationState.state}')
    if [[ $status == "COMPLETED" ]]; then
        echo "Application is completed."
        break
    fi
    if [[ $status == "FAILED" || $status == "UNKNOWN" ]]; then
        echo "Application is not in a running state. Current status: $status"
        exit 1
    fi
    if [[ $elapsed -ge $TIMEOUT ]]; then
        echo "Timed out waiting for the application to finish."
        exit 1
    fi
    sleep $INTERVAL
    elapsed=$((elapsed + INTERVAL))
done