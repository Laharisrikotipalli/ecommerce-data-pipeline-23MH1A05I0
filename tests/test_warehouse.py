import os
import psycopg2
import pytest

pytestmark = pytest.mark.db

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def test_fact_table_exists():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'warehouse'
              AND table_name = 'fact_sales'
        )
    """)

    assert cur.fetchone()[0]

    cur.close()
    conn.close()

def test_fact_grain_matches_transaction_items():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM warehouse.fact_sales")
    fact_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM staging.transaction_items")
    item_count = cur.fetchone()[0]

    assert fact_count == item_count

    cur.close()
    conn.close()
