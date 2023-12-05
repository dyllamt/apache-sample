# docker images
kafka-producer-image:
	cd src/kafka; docker build -t kafka-producer .

spark-jobs-image:
	cd src/spark; docker build -t spark-jobs .

trino-queries-image:
	cd src/trino; docker build -t trino-queries .
