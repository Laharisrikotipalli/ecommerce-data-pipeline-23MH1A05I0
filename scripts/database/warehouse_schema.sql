-- Create Warehouse Schema
CREATE SCHEMA IF NOT EXISTS warehouse;

-- 1. Date Dimension (366 rows for 2024 Leap Year)
CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    day INT,
    month_name VARCHAR(20),
    day_name VARCHAR(20),
    week_of_year INT,
    is_weekend BOOLEAN
);

-- 2. Customer Dimension (SCD Type 2)
CREATE TABLE IF NOT EXISTS warehouse.dim_customers (
    dw_customer_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    is_current BOOLEAN DEFAULT TRUE,
    effective_date DATE DEFAULT CURRENT_DATE, -- Naming as per
    end_date DATE
);

-- 3. Product Dimension (SCD Type 2 support)
CREATE TABLE IF NOT EXISTS warehouse.dim_products (
    dw_product_id SERIAL PRIMARY KEY,
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(12,2),
    cost NUMERIC(12,2),
    is_current BOOLEAN DEFAULT TRUE,
    effective_date DATE DEFAULT CURRENT_DATE,
    end_date DATE
);

-- 4. Sales Fact Table (Grain: transaction_items)
CREATE TABLE IF NOT EXISTS warehouse.fact_sales (
    fact_sales_id SERIAL PRIMARY KEY,
    dw_customer_id INT REFERENCES warehouse.dim_customers(dw_customer_id),
    dw_product_id INT REFERENCES warehouse.dim_products(dw_product_id),
    transaction_id VARCHAR(20),
    transaction_date DATE REFERENCES warehouse.dim_date(date_key),
    quantity INT,
    line_total NUMERIC(12,2),
    profit NUMERIC(12,2)
);

-- 5. Required Aggregate Tables

-- Aggregate 1: Daily Sales
CREATE TABLE IF NOT EXISTS warehouse.agg_daily_sales (
    sale_date DATE PRIMARY KEY REFERENCES warehouse.dim_date(date_key),
    total_revenue NUMERIC(12,2),
    total_profit NUMERIC(12,2),
    transaction_count INT,
    customer_count INT
);

-- Aggregate 2: Product Performance
CREATE TABLE IF NOT EXISTS warehouse.agg_product_performance (
    dw_product_id INT PRIMARY KEY REFERENCES warehouse.dim_products(dw_product_id),
    total_quantity_sold INT,
    total_revenue NUMERIC(12,2),
    total_profit NUMERIC(12,2)
);

-- Aggregate 3: Customer Metrics
CREATE TABLE IF NOT EXISTS warehouse.agg_customer_metrics (
    dw_customer_id INT PRIMARY KEY REFERENCES warehouse.dim_customers(dw_customer_id),
    total_spend NUMERIC(12,2),
    total_orders INT,
    last_order_date DATE
);