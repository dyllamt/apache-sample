import pyspark
from delta import DeltaTable
from pyspark.sql import types


table_name = "aggregate"
aggregate_schema = types.StructType(
    [
        types.StructField("timestamp", dataType=types.TimestampType(), nullable=False),
        types.StructField("count", dataType=types.StringType(), nullable=False),
        types.StructField("average", dataType=types.LongType(), nullable=False),
    ]
)


def main(source_path: str, destination_path: str):
    spark = (
        pyspark.sql.SparkSession.builder
        .appName(table_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )
    aggregate_job = (  # noqa
        spark.read  # reads from delta
        .format("delta")
        .load(source_path)
        .write  # writes to delta
        .format("delta")
        .mode("overwrite")
        .save(destination_path)
    )


if __name__ == "__main__":
    SOURCE_PATH = "/mnt/data/spark/delta/ingest"
    DESTINATION_PATH = "/mnt/data/spark/delta/aggregate"
    main(source_path=SOURCE_PATH, destination_path=DESTINATION_PATH)
