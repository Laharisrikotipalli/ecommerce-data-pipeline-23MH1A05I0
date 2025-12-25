import pandas as pd
from sqlalchemy import create_engine, text
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Functional Requirement 2: Use environment variables
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def ingest_all_data():
    engine = create_engine(DB_URL)
    summary = {"ingestion_timestamp": datetime.now().isoformat(), "tables_loaded": {}}
    
    # Functional Requirement 1: Source all 4 CSVs
    datasets = {
        "customers": "data/raw/customers.csv",
        "products": "data/raw/products.csv",
        "transactions": "data/raw/transactions.csv",
        "transaction_items": "data/raw/transaction_items.csv"
    }

    try:
        # Transaction Atomicity: Start a single transaction for all tables
        with engine.begin() as conn:
            for table, path in datasets.items():
                # Error Handling: Graceful handling of missing files
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Missing mandatory file: {path}")
                
                df = pd.read_csv(path)
                
                # Loading Strategy: Truncate before loading (Idempotency)
                conn.execute(text(f"TRUNCATE TABLE staging.{table} CASCADE;"))
                
                # Bulk Loading: Use 'multi' method for performance (>100 rows/sec)
                df.to_sql(
                    name=table, 
                    con=conn, 
                    schema='staging', 
                    if_exists='append', 
                    index=False, 
                    method='multi', 
                    chunksize=1000 # Performance Optimization
                )
                
                summary["tables_loaded"][f"staging.{table}"] = {
                    "rows_loaded": len(df),
                    "status": "success"
                }
                print(f"✓ Ingested {len(df)} rows into staging.{table}")

        # Summary Report: Generate the mandatory JSON file
        with open('data/staging/ingestion_summary.json', 'w') as f:
            json.dump(summary, f, indent=4)
            
    except Exception as e:
        # Transaction Atomicity: Rollback happens automatically here if any table fails
        print(f"CRITICAL ERROR: {e}. No data was loaded.")
        raise

if __name__ == "__main__":
    os.makedirs('data/staging', exist_ok=True)
    ingest_all_data()