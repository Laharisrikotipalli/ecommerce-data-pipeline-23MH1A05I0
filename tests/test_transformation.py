import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "ecommerce_db",
    "user": "admin",
    "password": "password"
}

def test_no_orphan_transactions():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM production.transactions t
        LEFT JOIN production.customers c
        ON t.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)

    assert cur.fetchone()[0] == 0
    conn.close()


def test_product_price_positive():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM production.products
        WHERE price <= 0
    """)

    assert cur.fetchone()[0] == 0
    conn.close()
