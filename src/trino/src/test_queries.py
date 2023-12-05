from trino.dbapi import connect


def execute_query(query):
    # Trino connection details
    conn = connect(
        host="trino-service",
        port=8080,
        user="init-job",
        catalog="delta",  # Make sure this matches your Delta Lake catalog
        schema="default",
    )
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def main():
    # Query for the 'ingest' table
    ingest_query = "SELECT * FROM delta.default.ingest LIMIT 10"
    ingest_rows = execute_query(ingest_query)
    print("Ingest Table Data:")
    for row in ingest_rows:
        print(row)

    # Query for the 'aggregate' table
    aggregate_query = "SELECT * FROM delta.default.aggregate LIMIT 10"
    aggregate_rows = execute_query(aggregate_query)
    print("\nAggregate Table Data:")
    for row in aggregate_rows:
        print(row)


if __name__ == "__main__":
    main()
