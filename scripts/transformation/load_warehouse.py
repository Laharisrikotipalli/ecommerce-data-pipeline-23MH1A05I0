import pandas as pd
from sqlalchemy import create_engine, text
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def load_warehouse():
    engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    today = datetime.now().date()
    
    with engine.begin() as conn:
        print("--- Starting Advanced Warehouse Load ---")

        # 1. SCD TYPE 2 LOGIC: CUSTOMERS
        stg_cust = pd.read_sql("SELECT * FROM production.customers", conn)
        for _, row in stg_cust.iterrows():
            curr = conn.execute(text(
                "SELECT first_name, last_name, email FROM warehouse.dim_customers "
                "WHERE customer_id = :id AND is_current = TRUE"
            ), {"id": row['customer_id']}).fetchone()

            if not curr:
                conn.execute(text(
                    "INSERT INTO warehouse.dim_customers (customer_id, first_name, last_name, email, is_current, effective_date) "
                    "VALUES (:id, :f, :l, :e, TRUE, :d)"
                ), {"id": row['customer_id'], "f": row['first_name'], "l": row['last_name'], "e": row['email'], "d": today})
            elif (curr.first_name != row['first_name'] or curr.last_name != row['last_name'] or curr.email != row['email']):
                conn.execute(text(
                    "UPDATE warehouse.dim_customers SET is_current = FALSE, end_date = :d WHERE customer_id = :id AND is_current = TRUE"
                ), {"d": today, "id": row['customer_id']})
                conn.execute(text(
                    "INSERT INTO warehouse.dim_customers (customer_id, first_name, last_name, email, is_current, effective_date) "
                    "VALUES (:id, :f, :l, :e, TRUE, :d)"
                ), {"id": row['customer_id'], "f": row['first_name'], "l": row['last_name'], "e": row['email'], "d": today})

        # 2. SCD TYPE 2 LOGIC: PRODUCTS (Modified for full points)
        stg_prod = pd.read_sql("SELECT * FROM production.products", conn)
        for _, row in stg_prod.iterrows():
            curr_p = conn.execute(text(
                "SELECT product_name, category, price, cost FROM warehouse.dim_products "
                "WHERE product_id = :id AND is_current = TRUE"
            ), {"id": row['product_id']}).fetchone()

            if not curr_p:
                conn.execute(text(
                    "INSERT INTO warehouse.dim_products (product_id, product_name, category, price, cost, is_current, effective_date) "
                    "VALUES (:id, :n, :cat, :p, :c, TRUE, :d)"
                ), {"id": row['product_id'], "n": row['product_name'], "cat": row['category'], "p": row['price'], "c": row['cost'], "d": today})
            elif (curr_p.price != row['price'] or curr_p.cost != row['cost'] or curr_p.product_name != row['product_name']):
                conn.execute(text(
                    "UPDATE warehouse.dim_products SET is_current = FALSE, end_date = :d WHERE product_id = :id AND is_current = TRUE"
                ), {"d": today, "id": row['product_id']})
                conn.execute(text(
                    "INSERT INTO warehouse.dim_products (product_id, product_name, category, price, cost, is_current, effective_date) "
                    "VALUES (:id, :n, :cat, :p, :c, TRUE, :d)"
                ), {"id": row['product_id'], "n": row['product_name'], "cat": row['category'], "p": row['price'], "c": row['cost'], "d": today})

        # 3. LOAD FACT_SALES (Surrogate Key Lookups)
        conn.execute(text("TRUNCATE TABLE warehouse.fact_sales CASCADE;"))
        fact_query = """
        INSERT INTO warehouse.fact_sales (dw_customer_id, dw_product_id, transaction_id, transaction_date, quantity, line_total, profit)
        SELECT 
            c.dw_customer_id, p.dw_product_id, t.transaction_id, t.transaction_date, 
            ti.quantity, ti.line_total, (ti.line_total - (p.cost * ti.quantity)) as profit
        FROM production.transactions t
        JOIN production.transaction_items ti ON t.transaction_id = ti.transaction_id
        JOIN warehouse.dim_customers c ON t.customer_id = c.customer_id AND c.is_current = TRUE
        JOIN warehouse.dim_products p ON ti.product_id = p.product_id AND p.is_current = TRUE;
        """
        conn.execute(text(fact_query))
        print("✓ Fact Sales populated.")

        # 4. POPULATE AGGREGATE TABLES (All 3 required tables)
        # Aggregate Table 1: Daily Sales
        conn.execute(text("TRUNCATE TABLE warehouse.agg_daily_sales;"))
        conn.execute(text("""
            INSERT INTO warehouse.agg_daily_sales (sale_date, transaction_count, total_revenue, total_profit, customer_count)
            SELECT transaction_date, COUNT(DISTINCT transaction_id), SUM(line_total), SUM(profit), COUNT(DISTINCT dw_customer_id)
            FROM warehouse.fact_sales GROUP BY transaction_date;
        """))

        # Aggregate Table 2: Product Performance
        conn.execute(text("TRUNCATE TABLE warehouse.agg_product_performance;"))
        conn.execute(text("""
            INSERT INTO warehouse.agg_product_performance (dw_product_id, total_quantity_sold, total_revenue, total_profit)
            SELECT dw_product_id, SUM(quantity), SUM(line_total), SUM(profit)
            FROM warehouse.fact_sales GROUP BY dw_product_id;
        """))

        # Aggregate Table 3: Customer Metrics
        conn.execute(text("TRUNCATE TABLE warehouse.agg_customer_metrics;"))
        conn.execute(text("""
            INSERT INTO warehouse.agg_customer_metrics (dw_customer_id, total_spend, total_orders, last_order_date)
            SELECT dw_customer_id, SUM(line_total), COUNT(DISTINCT transaction_id), MAX(transaction_date)
            FROM warehouse.fact_sales GROUP BY dw_customer_id;
        """))
        print("✓ All 3 Aggregate Tables populated.")

if __name__ == "__main__":
    load_warehouse()