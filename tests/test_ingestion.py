import os
import pytest
import psycopg2
import pytest

pytestmark = pytest.mark.db


import os

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "ecommerce_db",
    "user": "admin",
    "password": "password"
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
    conn.close()

def test_fact_grain_matches_transaction_items():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM warehouse.fact_sales")
    fact_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM staging.transaction_items")
    item_count = cur.fetchone()[0]

    assert fact_count == item_count
    conn.close()
