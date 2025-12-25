-- Create the three mandatory schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS production;
CREATE SCHEMA IF NOT EXISTS warehouse;

-- 1. Customers Table (Updated to match CSV columns: name, address, signup_date)
DROP TABLE IF EXISTS staging.customers; -- Clean start to fix the column error
CREATE TABLE staging.customers (
    customer_id VARCHAR(20),
    name VARCHAR(200),       -- Match CSV 'name'
    email VARCHAR(150),
    phone VARCHAR(50),
    address TEXT,            -- Match CSV 'address'
    signup_date DATE,        -- Match CSV 'signup_date'
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Mandatory Audit Column
);

-- 2. Products Table (Keep as is if CSV matches)
CREATE TABLE IF NOT EXISTS staging.products (
    product_id VARCHAR(20),
    product_name VARCHAR(200),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    brand VARCHAR(100),
    stock_quantity INTEGER,
    supplier_id VARCHAR(20),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Transactions Table
CREATE TABLE IF NOT EXISTS staging.transactions (
    transaction_id VARCHAR(20),
    customer_id VARCHAR(20),
    transaction_date DATE,
    transaction_time TIME,
    payment_method VARCHAR(50),
    shipping_address TEXT,
    total_amount DECIMAL(12,2),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Transaction Items Table (Updated to match CSV columns)
DROP TABLE IF EXISTS staging.transaction_items; 
CREATE TABLE staging.transaction_items (
    transaction_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity INTEGER,
    price_at_time DECIMAL(10,2), -- Match CSV column 'price_at_time'
    line_total DECIMAL(12,2),    -- Match CSV column 'line_total'
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Mandatory Audit Column
);