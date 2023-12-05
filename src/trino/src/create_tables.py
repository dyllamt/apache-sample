from trino.dbapi import connect  # type: ignore


def register_trino_tables():
    # Trino connection details
    conn = connect(
        host="trino-service",
        port=8080,
        user="init-job",
        catalog="delta",  # Make sure this matches your Delta Lake catalog
        schema="default",
    )
    cur = conn.cursor()

    # Register 'ingest' table
    cur.execute("""
        CALL delta.system.register_table(
            schema_name => 'default',
            table_name => 'ingest',
            table_location => 'file:///tmp/delta/ingest'
        )
    """)

    # Register 'aggregate' table
    cur.execute("""
        CALL delta.system.register_table(
            schema_name => 'default',
            table_name => 'aggregate',
            table_location => 'file:///tmp/delta/aggregate'
        )
    """)

    print("Tables registered in Trino")


if __name__ == "__main__":
    register_trino_tables()
