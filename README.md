# apache-sample
An apache data application on kubernetes.

## System Design

![](system-design.png)

`Kafka` event source to ingest realtime application data

`Spark` framework for microbatch and batch processes

`Airflow` orchestration of microbatch and batch processes

`Delta` ACID-compliant storage layer on file storage

`Trino` analytics query engine for ad-hoc analysis

## System Tests

An end-to-end test of the system can be run from minikube. The application:

1. publishes sample data to a test topic on the kafka cluster
2. ingests the data into a staging table on delta using structured-streaming
3. performs windowed aggregations on the data and saves the results
4. triggers a sql query through trino to simulate an end-user

The tests can be triggered from the tests module with pytest.


## Developer Notes

Ensure docker desktop is running
```shell
open -a Docker
```

Build docker images for the kafka producer and spark jobs
```shell
make kafka-producer-image
make spark-jobs-image
```

Activate the local kubernetes context and install required operators
```shell
kubectl config use-context docker-desktop

```

Deploy the kafka broker and delta storage to the cluster
```shell
make kafka-broker-chart
make delta-storage-chart
```

Deploy the spark streaming job to the cluster
```shell
make spark-ingest-job
```

Deploy the kafka producer job to the cluster
```shell
make kafka-producer-job
```

Deploy the spark batch job to the cluster
```shell
make spark-aggregate-job
```
