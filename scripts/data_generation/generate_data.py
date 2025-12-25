import pandas as pd
import random
from faker import Faker
from datetime import datetime
import json

fake = Faker()

# ----------------------------
# CUSTOMER GENERATION
# ----------------------------
def generate_customers(num_customers: int) -> pd.DataFrame:
    customers = []
    for i in range(num_customers):
        customers.append({
            "customer_id": f"CUST{i+1:05d}",
            "name": fake.name(),
            "email": fake.email(),
            "city": fake.city(),
            "state": fake.state(),
            "country": fake.country(),
            "created_at": fake.date_time_this_decade()
        })
    return pd.DataFrame(customers)


# ----------------------------
# PRODUCT GENERATION
# ----------------------------
def generate_products(num_products: int) -> pd.DataFrame:
    categories = ["Electronics", "Clothing", "Home", "Books", "Sports"]
    products = []
    for i in range(num_products):
        products.append({
            "product_id": f"PROD{i+1:05d}",
            "product_name": fake.word().title(),
            "category": random.choice(categories),
            "price": round(random.uniform(10, 500), 2)
        })
    return pd.DataFrame(products)


# ----------------------------
# TRANSACTION GENERATION
# ----------------------------
def generate_transactions(num_transactions: int, customers_df: pd.DataFrame) -> pd.DataFrame:
    payment_methods = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash"]
    transactions = []

    for i in range(num_transactions):
        customer = customers_df.sample(1).iloc[0]
        date = fake.date_this_year()

        transactions.append({
            "transaction_id": f"TXN{i+1:06d}",
            "customer_id": customer["customer_id"],
            "transaction_date": date,
            "transaction_time": fake.time(),
            "payment_method": random.choice(payment_methods),
            "shipping_address": fake.address(),
            "total_amount": 0.0  # will be recalculated later
        })

    return pd.DataFrame(transactions)


# ----------------------------
# TRANSACTION ITEMS
# ----------------------------
def generate_transaction_items(transactions_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
    items = []

    for _, txn in transactions_df.iterrows():
        num_items = random.randint(1, 5)
        selected_products = products_df.sample(num_items)

        total_amount = 0

        for _, prod in selected_products.iterrows():
            quantity = random.randint(1, 3)
            line_total = round(quantity * prod["price"], 2)
            total_amount += line_total

            items.append({
                "transaction_id": txn["transaction_id"],
                "product_id": prod["product_id"],
                "quantity": quantity,
                "price_at_time": prod["price"],
                "line_total": line_total
            })

        transactions_df.loc[
            transactions_df["transaction_id"] == txn["transaction_id"],
            "total_amount"
        ] = round(total_amount, 2)

    return pd.DataFrame(items)


# ----------------------------
# REFERENTIAL INTEGRITY CHECK
# ----------------------------
def validate_referential_integrity(customers, products, transactions, items) -> dict:
    return {
        "customers": int(len(customers)),
        "products": int(len(products)),
        "transactions": int(len(transactions)),
        "transaction_items": int(len(items)),
        "customer_fk_valid": bool(transactions["customer_id"].isin(customers["customer_id"]).all()),
        "product_fk_valid": bool(items["product_id"].isin(products["product_id"]).all()),
        "transaction_fk_valid": bool(items["transaction_id"].isin(transactions["transaction_id"]).all())
    }


# ----------------------------
# MAIN EXECUTION
# ----------------------------
if __name__ == "__main__":
    customers_df = generate_customers(100)
    products_df = generate_products(50)
    transactions_df = generate_transactions(300, customers_df)
    items_df = generate_transaction_items(transactions_df, products_df)

    metadata = validate_referential_integrity(
        customers_df, products_df, transactions_df, items_df
    )

    # Save CSVs
    customers_df.to_csv("data/raw/customers.csv", index=False)
    products_df.to_csv("data/raw/products.csv", index=False)
    transactions_df.to_csv("data/raw/transactions.csv", index=False)
    items_df.to_csv("data/raw/transaction_items.csv", index=False)

    # Save metadata
    with open("data/raw/generation_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print("✅ Data generation completed successfully")
