INSERT INTO warehouse.fact_sales (
    sales_key,
    date_key,
    customer_key,
    product_key,
    payment_method_key,
    transaction_id,
    quantity,
    unit_price,
    discount_amount,
    line_total,
    profit,
    created_at
)
SELECT
    ti.item_id                     AS sales_key,
    d.date_key                     AS date_key,
    dc.customer_key                AS customer_key,
    dp.product_key                 AS product_key,
    pm.payment_method_key          AS payment_method_key,
    t.transaction_id,
    ti.quantity,
    ti.price_at_time               AS unit_price,
    0                              AS discount_amount,
    ti.line_total,
    ti.line_total                  AS profit,
    t.created_at
FROM production.transaction_items ti
JOIN production.transactions t
  ON ti.transaction_id = t.transaction_id
JOIN warehouse.dim_date d
  ON d.full_date = t.transaction_date
JOIN warehouse.dim_customers dc
  ON dc.customer_id = t.customer_id
 AND dc.is_current = true
JOIN warehouse.dim_products dp
  ON dp.product_id = ti.product_id
 AND dp.is_current = true
JOIN warehouse.dim_payment_method pm
  ON pm.payment_method_name = t.payment_method;
