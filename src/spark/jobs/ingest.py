import pyspark
from delta import DeltaTable
from pyspark.sql import types


table_name = "ingest"
ingest_schema = types.StructType(
    [
        types.StructField("uid", dataType=types.StringType(), nullable=False),
        types.StructField("timestamp", dataType=types.TimestampType(), nullable=False),
        types.StructField("value", dataType=types.LongType(), nullable=False),
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
    ingest_table = (  # noqa
        DeltaTable.createIfNotExists(spark)
        .tableName(table_name)
        .addColummns(ingest_schema)
        .location(delta_path)
        .execute()
    )
    ingest_stream = (
        spark.readStream  # reads from kafka
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_server)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "earliest")
        .load()
        .writeStream  # writes to delta
        .trigger(processingTime="10 seconds")
        .format("delta")
        .outputMode("append")
        .start(delta_path)
    )
    ingest_stream.awaitTermination()


if __name__ == "__main__":
    KAFKA_SERVER = "kafka://thing"
    DELTA_PATH = "/mnt/data/spark/delta/ingest"
    main(kafka_server=KAFKA_SERVER, delta_path=DELTA_PATH)
