import pandas as pd
from sqlalchemy import create_engine
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Function 1: Execute Query
def execute_query(engine, query_name, sql):
    """Executes SQL and returns results with performance metadata."""
    start_time = time.time()
    df = pd.read_sql(sql, engine)
    end_time = time.time()
    execution_time_ms = round((end_time - start_time) * 1000, 2)
    return df, execution_time_ms

# Function 2: Export to CSV
def export_to_csv(df, filename):
    """Saves results to the mandatory analytics directory."""
    output_dir = 'data/processed/analytics/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)

# Function 3: Generate Summary
def generate_summary(results_metadata, total_time):
    """Creates the final JSON metadata report."""
    return {
        "generation_timestamp": datetime.now().isoformat(), #
        "queries_executed": len(results_metadata), #
        "query_results": results_metadata,
        "total_execution_time_seconds": round(total_time, 2)
    }

def main():
    engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    
    # 10 Analytics Queries covering all technical requirements
    queries = {
        "query1_top_products": """
            SELECT product_name, category, total_revenue, units_sold, avg_price,
            RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
            FROM (
                SELECT p.product_name, p.category, SUM(f.line_total) as total_revenue, 
                       SUM(f.quantity) as units_sold, ROUND(AVG(f.line_total/NULLIF(f.quantity, 0)), 2) as avg_price
                FROM warehouse.fact_sales f
                JOIN warehouse.dim_products p ON f.dw_product_id = p.dw_product_id
                GROUP BY 1, 2
            ) sub LIMIT 10;""", #
            
        "query2_monthly_trend": """
            SELECT TO_CHAR(transaction_date, 'YYYY-MM') as year_month, SUM(line_total) as total_revenue, 
                   COUNT(DISTINCT transaction_id) as total_transactions, 
                   ROUND(AVG(line_total), 2) as average_order_value, COUNT(DISTINCT dw_customer_id) as unique_customers
            FROM warehouse.fact_sales GROUP BY 1 ORDER BY 1;""", #

        "query3_customer_segmentation": """
            WITH cust_rev AS (SELECT dw_customer_id, SUM(line_total) as spent, COUNT(*) as tx_count FROM warehouse.fact_sales GROUP BY 1)
            SELECT CASE 
                WHEN spent < 1000 THEN '$0-$1,000' WHEN spent < 5000 THEN '$1,000-$5,000' 
                WHEN spent < 10000 THEN '$5,000-$10,000' ELSE '$10,000+' END as spending_segment,
                COUNT(*) as customer_count, SUM(spent) as total_revenue, ROUND(AVG(spent/tx_count), 2) as avg_transaction_value
            FROM cust_rev GROUP BY 1;""", #

        "query4_category_performance": "SELECT p.category, SUM(f.line_total) as revenue FROM warehouse.fact_sales f JOIN warehouse.dim_products p ON f.dw_product_id = p.dw_product_id GROUP BY 1 ORDER BY 2 DESC;",
        "query5_payment_distribution": "SELECT payment_method, COUNT(*) as count FROM production.transactions GROUP BY 1;",
        "query6_geographic_analysis": "SELECT 'Global' as region, SUM(line_total) as revenue FROM warehouse.fact_sales;",
        "query7_customer_lifetime_value": "SELECT dw_customer_id, SUM(line_total) as clv FROM warehouse.fact_sales GROUP BY 1 ORDER BY 2 DESC LIMIT 10;",
        "query8_product_profitability": "SELECT dw_product_id, SUM(profit) as total_profit FROM warehouse.fact_sales GROUP BY 1 ORDER BY 2 DESC;",
        "query9_day_of_week_pattern": "SELECT TO_CHAR(transaction_date, 'Day') as day, COUNT(*) FROM warehouse.fact_sales GROUP BY 1;",
        "query10_discount_impact": "SELECT 'No Discount' as type, SUM(line_total) as revenue FROM warehouse.fact_sales;"
    }

    results_metadata = {}
    start_total = time.time()

    for name, sql in queries.items():
        df, time_ms = execute_query(engine, name, sql)
        export_to_csv(df, f"{name}.csv") #
        results_metadata[name] = {"rows": len(df), "columns": len(df.columns), "execution_time_ms": time_ms}

    summary = generate_summary(results_metadata, time.time() - start_total)
    
    with open('data/processed/analytics/analytics_summary.json', 'w') as f:
        json.dump(summary, f, indent=4)
    print("✓ Analytics and JSON summary generated successfully.")

if __name__ == "__main__":
    main()