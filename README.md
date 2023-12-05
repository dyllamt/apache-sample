# apache-sample
Apache data system written for development in a local cluster and incramental deployment modifications for production environments. Great for learning about cloud-native development in the apache software ecosystem.

## System Design

![](system-design.png)

- `Kafka` event source to ingest realtime application data
- `Spark` framework for microbatch and batch processes
- `Delta` ACID-compliant storage layer on file storage
- `Hive` metadata store for the delta schemas
- `Trino` analytics query engine for ad-hoc analysis

## System Tests

An end-to-end test of the system can be run in kubernetes. The test:

1. publishes sample data to a topic on the kafka cluster
2. ingests the data into a staging table on delta using structured-streaming
3. performs windowed aggregations on the data and saves the results
4. triggers a sql analytics query through trino to simulate an analyst

The tests are triggered through github actions, although you will need to use a self-hosted runner.


## Developer Notes

### Testing in the Development Environment
Ensure docker desktop is running
```shell
open -a Docker;
kubectl config use-context docker-desktop
```

Build docker images for the kafka, spark, and trino jobs
```shell
make kafka-producer-image;
make spark-jobs-image;
make trino-queries-image
```

Run the system test
```shell
cd scripts;
./01-install-operators.sh;
./02-deploy-kafka.sh;
./03-deploy-delta-trino.sh;
./04-run-spark-jobs.sh;
./05-run-trino-query.sh
```


### Modifying for a Production Environment

1. Scale the kafka cluster and spark streaming jobs
2. Change the batch job deployment to run on an ephemeral cluster
3. Change the storage configuration to cloud storage
4. Update the hive metastore to postgresql
5. Scale the trino cluster for more performant queries
6. Setup an orchestrator such as Airflow or Prefect
7. Configure security and monitoring for the application


## Updates

Checkout this open-source project and company: [stackable](https://stackable.tech/en/).
