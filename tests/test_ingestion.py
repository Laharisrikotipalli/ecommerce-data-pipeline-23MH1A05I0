import os
import pytest

# 🚫 Skip DB tests locally
if not os.getenv("CI"):
    pytest.skip("Skipping DB tests locally", allow_module_level=True)

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "ecommerce_db",
    "user": "admin",
    "password": "password"
}

def test_database_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    assert conn is not None
    conn.close()

def test_staging_tables_exist():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    tables = ["customers", "products", "transactions", "transaction_items"]

    for table in tables:
        cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'staging'
                  AND table_name = %s
            )
        """, (table,))
        assert cur.fetchone()[0]

    conn.close()
