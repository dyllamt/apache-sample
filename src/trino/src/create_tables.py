from trino.dbapi import connect


def create_trino_tables():
    # Trino connection details
    conn = connect(
        host="trino-service",
        port=8080,
        user="init-job",
        catalog="hive",
        schema="default",
    )
    cur = conn.cursor()

    # SQL to create 'ingest' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hive.default.ingest (
            uid VARCHAR,
            timestamp TIMESTAMP,
            value DOUBLE
        ) WITH (
            external_location = 'file:///tmp/delta/ingest',
            format = 'DELTA'
        )
    """)

    # SQL to create 'aggregate' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hive.default.aggregate (
            timestamp TIMESTAMP,
            count BIGINT,
            average DOUBLE
        ) WITH (
            external_location = 'file:///tmp/delta/aggregate',
            format = 'DELTA'
        )
    """)

    print("Tables created in Trino")


if __name__ == "__main__":
    create_trino_tables()
