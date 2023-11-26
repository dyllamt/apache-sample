# docker images
airflow-dags-image:
	cd src/airflow-dags; docker build -t airflow-dags .

kafka-producer-image:
	cd src/kafka-producer; docker build -t kafka-producer .

spark-jobs-image:
	cd src/spark; docker build -t spark-jobs .

# systems tests