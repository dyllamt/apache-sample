import pyspark
from pyspark.sql import types, functions
from pyspark.sql.window import Window


table_name = "aggregate"
aggregate_schema = types.StructType(
    [
        types.StructField("timestamp", dataType=types.TimestampType(), nullable=False),
        types.StructField("count", dataType=types.LongType(), nullable=False),
        types.StructField("average", dataType=types.FloatType(), nullable=False),
    ]
)
window_duration = "1 second"


def main(source_path: str, destination_path: str):
    spark = (
        pyspark.sql.SparkSession.builder
        .appName(table_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )
    create_job = (  # noqa
        spark.createDataFrame([], aggregate_schema)
        .write
        .format("delta")
        .mode("ignore")
        .save(destination_path)
    )
    aggregate_job = (  # noqa
        spark.read  # reads from delta
        .format("delta")
        .load(source_path)
        .withColumn("timestamp", functions.to_timestamp("timestamp"))
        .groupBy(functions.window("timestamp", window_duration))
        .agg(
            functions.count("value").alias("count"),
            functions.avg("value").alias("average")
        )
        .select(
            functions.col("window.start").alias("timestamp"),
            "count",
            "average"
        )
        .write  # writes to delta
        .format("delta")
        .mode("overwrite")
        .save(destination_path)
    )


if __name__ == "__main__":
    import os

    SOURCE_PATH = os.environ.get("DELTA_INGEST_LOCATION", "")
    DESTINATION_PATH = os.environ.get("DELTA_AGGREGATE_LOCATION", "")

    main(source_path=SOURCE_PATH, destination_path=DESTINATION_PATH)
