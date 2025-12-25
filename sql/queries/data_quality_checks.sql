-- 1. Completeness: Check for missing mandatory business fields
SELECT 'customers' as table, 'email' as column, count(*) as violations 
FROM staging.customers WHERE email IS NULL OR email = '';

-- 2. Uniqueness: Identify duplicate business keys
SELECT email, count(*) as duplicate_count 
FROM staging.customers GROUP BY email HAVING count(*) > 1;

-- 3. Referential Integrity: Find orphan records (transaction_id not found)
SELECT count(*) as orphan_transactions 
FROM staging.transactions t
LEFT JOIN staging.customers c ON t.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 4. Business Rules: Validate calculated fields (line_total = qty * price)
SELECT item_id, line_total, (quantity * price_at_time) as expected 
FROM staging.transaction_items 
WHERE ABS(line_total - (quantity * price_at_time)) > 0.01;