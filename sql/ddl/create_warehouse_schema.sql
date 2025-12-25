CREATE SCHEMA IF NOT EXISTS warehouse;

-- 1. Date Dimension (Populated via Python for 2024 Leap Year)
DROP TABLE IF EXISTS warehouse.dim_date CASCADE;
CREATE TABLE warehouse.dim_date (
    date_key INTEGER PRIMARY KEY, -- Format: YYYYMMDD
    full_date DATE UNIQUE,
    year INT,
    quarter INT,
    month INT,
    day INT,
    month_name VARCHAR(20),
    day_name VARCHAR(20),
    week_of_year INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN DEFAULT FALSE -- Optional but recommended
);

-- 2. Customer Dimension (SCD Type 2 Tracking)
DROP TABLE IF EXISTS warehouse.dim_customers CASCADE;
CREATE TABLE warehouse.dim_customers (
    customer_key SERIAL PRIMARY KEY, -- Surrogate Key
    customer_id VARCHAR(20),          -- Business Key
    full_name VARCHAR(200),
    email VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    age_group VARCHAR(20),
    customer_segment VARCHAR(20),    -- Derived: New, Regular, VIP
    registration_date DATE,
    effective_date DATE,             -- SCD Type 2
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- 3. Product Dimension (Denormalized descriptive attributes)
DROP TABLE IF EXISTS warehouse.dim_products CASCADE;
CREATE TABLE warehouse.dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(20),
    product_name VARCHAR(200),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    brand VARCHAR(100),
    price_range VARCHAR(20),         -- Denormalized: Budget, Mid-range, Premium
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- 4. Payment Method Dimension
DROP TABLE IF EXISTS warehouse.dim_payment_method CASCADE;
CREATE TABLE warehouse.dim_payment_method (
    payment_method_key SERIAL PRIMARY KEY,
    payment_method_name VARCHAR(50),
    payment_type VARCHAR(20)         -- Categorize: Online or Offline
);

-- 5. Sales Fact Table (Process Metrics & Measures)
DROP TABLE IF EXISTS warehouse.fact_sales CASCADE;
CREATE TABLE warehouse.fact_sales (
    sales_key BIGSERIAL PRIMARY KEY, -- Surrogate key for fact
    date_key INTEGER NOT NULL REFERENCES warehouse.dim_date(date_key),
    customer_key INTEGER NOT NULL REFERENCES warehouse.dim_customers(customer_key),
    product_key INTEGER NOT NULL REFERENCES warehouse.dim_products(product_key),
    payment_method_key INTEGER NOT NULL REFERENCES warehouse.dim_payment_method(payment_method_key),
    transaction_id VARCHAR(20),      -- Degenerate Dimension
    quantity INTEGER,                -- Additive Measure
    unit_price DECIMAL(12,2),        -- Measure
    discount_amount DECIMAL(12,2),   -- Calculated Measure
    line_total DECIMAL(12,2),        -- Additive Measure
    profit DECIMAL(12,2),            -- Calculated: line_total - (cost * quantity)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. AGGREGATE TABLES (For Performance Marks)
-- Daily Sales Aggregate
CREATE TABLE warehouse.agg_daily_sales (
    date_key INTEGER PRIMARY KEY,
    total_transactions INTEGER,
    total_revenue DECIMAL(15,2),
    total_profit DECIMAL(15,2),
    unique_customers INTEGER
);

-- Product Performance Aggregate
CREATE TABLE warehouse.agg_product_performance (
    product_key INTEGER PRIMARY KEY,
    total_quantity_sold INTEGER,
    total_revenue DECIMAL(15,2),
    total_profit DECIMAL(15,2),
    avg_discount_percentage DECIMAL(5,2)
);

-- Customer Metrics Aggregate
CREATE TABLE warehouse.agg_customer_metrics (
    customer_key INTEGER PRIMARY KEY,
    total_transactions INTEGER,
    total_spent DECIMAL(15,2),
    avg_order_value DECIMAL(12,2),
    last_purchase_date DATE
);

-- 7. PERFORMANCE INDEXES
CREATE INDEX idx_fact_date ON warehouse.fact_sales(date_key);
CREATE INDEX idx_fact_customer ON warehouse.fact_sales(customer_key);
CREATE INDEX idx_fact_product ON warehouse.fact_sales(product_key);