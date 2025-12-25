import os
import psycopg2

# Database configuration
# Uses environment variables in CI
# Falls back to local Docker defaults when running locally
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5433)),
    "dbname": os.getenv("DB_NAME", "ecommerce_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
}


def test_database_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    assert conn is not None
    conn.close()


def test_staging_tables_exist():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    tables = [
        "customers",
        "products",
        "transactions",
        "transaction_items"
    ]

    for table in tables:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'staging'
                  AND table_name = %s
            )
            """,
            (table,)
        )
        assert cur.fetchone()[0], f"{table} missing in staging schema"

    cur.close()
    conn.close()
