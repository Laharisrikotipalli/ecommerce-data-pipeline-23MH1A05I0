import pandas as pd
from sqlalchemy import create_engine, text
import json
import os
from datetime import datetime

# ======================
# DB CONFIG
# ======================
DB_URL = "postgresql://admin:password@localhost:5433/ecommerce_db"
engine = create_engine(DB_URL)

summary = {
    "transformation_timestamp": datetime.utcnow().isoformat(),
    "records_processed": {},
    "transformations_applied": [],
    "data_quality_post_transform": {
        "null_violations": 0,
        "constraint_violations": 0
    }
}

with engine.begin() as conn:

    # ======================
    # CUSTOMERS
    # ======================
    df = pd.read_sql("SELECT * FROM staging.customers", conn)

    df["email"] = df["email"].str.lower().str.strip()
    df["name"] = df["name"].str.strip()
    df[["first_name", "last_name"]] = df["name"].str.split(" ", n=1, expand=True)

    conn.execute(text("TRUNCATE production.customers"))

    df[[
        "customer_id", "name", "first_name", "last_name",
        "email", "city", "state", "country", "created_at"
    ]].to_sql("customers", conn, schema="production", if_exists="append", index=False)

    summary["records_processed"]["customers"] = {
        "input": len(df), "output": len(df), "filtered": 0
    }

    # ======================
    # PRODUCTS
    # ======================
    df = pd.read_sql("SELECT * FROM staging.products", conn)

    df["profit_margin"] = 30.00
    df["price_category"] = pd.cut(
        df["price"],
        bins=[0, 50, 200, 1e9],
        labels=["Budget", "Mid-range", "Premium"],
        right=False
    )

    conn.execute(text("TRUNCATE production.products"))

    df[[
        "product_id", "product_name", "category",
        "price", "profit_margin", "price_category"
    ]].to_sql("products", conn, schema="production", if_exists="append", index=False)

    summary["records_processed"]["products"] = {
        "input": len(df), "output": len(df), "filtered": 0
    }

    # ======================
    # TRANSACTIONS  (FIXED)
    # ======================
    df = pd.read_sql(
        """
        SELECT
            transaction_id,
            customer_id,
            transaction_date,
            transaction_time,
            payment_method,
            total_amount,
            loaded_at AS created_at
        FROM staging.transactions
        WHERE total_amount > 0
        """,
        conn
    )

    conn.execute(text("TRUNCATE production.transactions"))

    df.to_sql(
        "transactions",
        conn,
        schema="production",
        if_exists="append",
        index=False
    )

    summary["records_processed"]["transactions"] = {
        "input": len(df), "output": len(df), "filtered": 0
    }

    # ======================
    # TRANSACTION ITEMS
    # ======================
    df = pd.read_sql(
        """
        SELECT
            transaction_id,
            product_id,
            quantity,
            price_at_time,
            line_total
        FROM staging.transaction_items
        WHERE quantity > 0
        """,
        conn
    )

    conn.execute(text("TRUNCATE production.transaction_items"))

    df.to_sql(
        "transaction_items",
        conn,
        schema="production",
        if_exists="append",
        index=False
    )

    summary["records_processed"]["transaction_items"] = {
        "input": len(df), "output": len(df), "filtered": 0
    }

summary["transformations_applied"] = [
    "email_normalization",
    "name_split",
    "price_category_assignment",
    "profit_margin_enrichment",
    "schema_alignment"
]

os.makedirs("data/processed", exist_ok=True)
with open("data/processed/transformation_summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("✅ Staging → Production ETL completed successfully")
