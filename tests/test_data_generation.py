import os
import pandas as pd
import re

DATA_PATH = "data/raw"

def test_csv_files_exist():
    required_files = [
        "customers.csv",
        "products.csv",
        "transactions.csv",
        "transaction_items.csv"
    ]
    for f in required_files:
        assert os.path.exists(os.path.join(DATA_PATH, f)), f"{f} missing"


def test_mandatory_columns_exist():
    df = pd.read_csv(f"{DATA_PATH}/customers.csv")
    for col in ["customer_id", "email"]:
        assert col in df.columns


def test_no_null_customer_ids():
    df = pd.read_csv(f"{DATA_PATH}/customers.csv")
    assert df["customer_id"].isnull().sum() == 0


def test_email_format():
    df = pd.read_csv(f"{DATA_PATH}/customers.csv")
    pattern = r"[^@]+@[^@]+\.[^@]+"
    assert df["email"].str.match(pattern).all()

import numpy as np

def test_line_total_calculation():
    df = pd.read_csv(f"{DATA_PATH}/transaction_items.csv")

    calculated = df["quantity"] * df["price_at_time"]

    # Allow small floating point rounding differences
    assert np.allclose(
        calculated,
        df["line_total"],
        rtol=0.0,
        atol=0.01
    ), "Line total calculation mismatch beyond tolerance"
