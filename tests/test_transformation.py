import os
import psycopg2

# Database configuration
# Uses CI environment variables when available
# Falls back to local Docker configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5433)),
    "dbname": os.getenv("DB_NAME", "ecommerce_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
}


def test_no_orphan_transactions():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM production.transactions t
        LEFT JOIN production.customers c
          ON t.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    )

    assert cur.fetchone()[0] == 0

    cur.close()
    conn.close()


def test_product_price_positive():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM production.products
        WHERE price <= 0
        """
    )

    assert cur.fetchone()[0] == 0

    cur.close()
    conn.close()
