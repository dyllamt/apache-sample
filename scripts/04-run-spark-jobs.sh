# setup environmental variables for sources/sinks
kubectl apply -f ../k8s/spark/job-env-variables.yaml -n dev

# start structured streaming
kubectl apply -f ../k8s/spark/spark-application-ingest.yaml -n dev


# produce sample data for streaming
kubectl apply -f ../k8s/spark/kafka-producer-job.yaml -n dev

# run aggregation job
kubectl apply -f ../k8s/spark/spark-application-aggregate.yaml -n dev