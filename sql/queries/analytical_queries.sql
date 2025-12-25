-- Query 1: Top 10 Products by Revenue
-- Objective: Identify best-selling products
SELECT 
    p.product_name, 
    p.category, 
    SUM(f.line_total) as total_revenue, 
    SUM(f.quantity) as units_sold,
    ROUND(AVG(f.line_total/NULLIF(f.quantity, 0)), 2) as avg_price
FROM warehouse.fact_sales f
JOIN warehouse.dim_products p ON f.dw_product_id = p.dw_product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- Query 2: Monthly Sales Trend
-- Objective: Analyze revenue over time using dim_date
SELECT 
    TO_CHAR(transaction_date, 'YYYY-MM') as year_month,
    SUM(line_total) as total_revenue,
    COUNT(DISTINCT transaction_id) as total_transactions,
    COUNT(DISTINCT dw_customer_id) as unique_customers
FROM warehouse.fact_sales
GROUP BY year_month
ORDER BY year_month;

-- Query 3: Customer Segmentation Analysis
-- Objective: Group customers by spending patterns
WITH customer_revenue AS (
    SELECT dw_customer_id, SUM(line_total) as total_spent
    FROM warehouse.fact_sales
    GROUP BY dw_customer_id
)
SELECT 
    CASE 
        WHEN total_spent < 1000 THEN '$0-$1,000'
        WHEN total_spent < 5000 THEN '$1,000-$5,000'
        WHEN total_spent < 10000 THEN '$5,000-$10,000'
        ELSE '$10,000+'
    END as spending_segment,
    COUNT(*) as customer_count,
    SUM(total_spent) as total_revenue
FROM customer_revenue
GROUP BY spending_segment;
-- Query 4: Customer Lifetime Value (CLV)
-- Objective: Rank customers by their total historical spend
SELECT 
    c.first_name || ' ' || c.last_name as customer_name,
    COUNT(f.transaction_id) as total_orders,
    SUM(f.line_total) as lifetime_value,
    ROUND(AVG(f.line_total), 2) as average_order_value
FROM warehouse.fact_sales f
JOIN warehouse.dim_customers c ON f.dw_customer_id = c.dw_customer_id
WHERE c.is_current = TRUE
GROUP BY 1
ORDER BY lifetime_value DESC
LIMIT 10;

-- Query 5: Profit Margin by Product Category
-- Objective: Identify which categories are most profitable
SELECT 
    p.category,
    SUM(f.line_total) as total_revenue,
    SUM(f.profit) as total_profit,
    ROUND((SUM(f.profit) / NULLIF(SUM(f.line_total), 0)) * 100, 2) as margin_percentage
FROM warehouse.fact_sales f
JOIN warehouse.dim_products p ON f.dw_product_id = p.dw_product_id
GROUP BY 1
ORDER BY margin_percentage DESC;

-- Query 6: Payment Method Popularity
-- Objective: Analyze which payment methods drive the most volume
-- Note: Joining production.transactions for payment_method if not in dim_payment_method
SELECT 
    t.payment_method,
    COUNT(f.transaction_id) as transaction_count,
    SUM(f.line_total) as total_revenue
FROM warehouse.fact_sales f
JOIN production.transactions t ON f.transaction_id = t.transaction_id
GROUP BY 1
ORDER BY transaction_count DESC;

-- Query 7: Product Reorder Rate
-- Objective: Products with high quantity per transaction
SELECT 
    p.product_name,
    COUNT(f.transaction_id) as times_purchased,
    SUM(f.quantity) as total_units,
    ROUND(AVG(f.quantity), 2) as avg_units_per_order
FROM warehouse.fact_sales f
JOIN warehouse.dim_products p ON f.dw_product_id = p.dw_product_id
GROUP BY 1
HAVING COUNT(f.transaction_id) > 5
ORDER BY avg_units_per_order DESC;

-- Query 8: Daily Sales Velocity (Using Aggregate Table)
-- Objective: Use the aggregate table for high performance
SELECT 
    sale_date,
    transaction_count,
    total_revenue,
    ROUND(total_revenue / NULLIF(transaction_count, 0), 2) as revenue_per_tx
FROM warehouse.agg_daily_sales
WHERE sale_date > CURRENT_DATE - INTERVAL '30 days'
ORDER BY sale_date DESC;

-- Query 9: Underperforming Products (Low Revenue)
-- Objective: Identify products contributing less than 1% of total revenue
WITH total_rev AS (SELECT SUM(line_total) as grand_total FROM warehouse.fact_sales)
SELECT 
    p.product_name,
    SUM(f.line_total) as product_revenue,
    ROUND((SUM(f.line_total) / (SELECT grand_total FROM total_rev)) * 100, 4) as revenue_share_pct
FROM warehouse.fact_sales f
JOIN warehouse.dim_products p ON f.dw_product_id = p.dw_product_id
GROUP BY p.product_name
ORDER BY product_revenue ASC
LIMIT 10;

-- Query 10: Peak Transaction Days
-- Objective: Identify days of the week with highest activity
SELECT 
    TO_CHAR(transaction_date, 'Day') as day_of_week,
    COUNT(transaction_id) as total_transactions,
    SUM(line_total) as revenue
FROM warehouse.fact_sales
GROUP BY 1, EXTRACT(DOW FROM transaction_date)
ORDER BY EXTRACT(DOW FROM transaction_date);