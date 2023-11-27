import pyspark
from pyspark.sql import types, functions


table_name = "ingest"
ingest_schema = types.StructType(
    [
        types.StructField("uid", dataType=types.StringType(), nullable=False),
        types.StructField("timestamp", dataType=types.StringType(), nullable=False),
        types.StructField("value", dataType=types.FloatType(), nullable=False),
    ]
)


def main(kafka_server: str, delta_path: str, kafka_topic: str = "sample"):
    spark = (
        pyspark.sql.SparkSession.builder
        .appName(table_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )
    create_job = (  # noqa
        spark.createDataFrame([], ingest_schema)
        .write
        .format("delta")
        .mode("ignore")
        .save(delta_path)
    )
    ingest_stream = (
        spark.readStream  # reads from kafka
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_server)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "earliest")
        .load()
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        .select(functions.from_json("value", ingest_schema).alias("data"))
        .select("data.*")
        .writeStream  # writes to delta
        .option("checkpointLocation", "file:///tmp/checkpoints/ingest")
        .trigger(processingTime="10 seconds")
        .format("delta")
        .outputMode("append")
        .start(delta_path)
    )
    ingest_stream.awaitTermination()


if __name__ == "__main__":
    import os

    KAFKA_SERVER = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
    KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "")
    DELTA_PATH = os.environ.get("DELTA_INGEST_LOCATION", "")

    main(kafka_server=KAFKA_SERVER, delta_path=DELTA_PATH, kafka_topic=KAFKA_TOPIC)
