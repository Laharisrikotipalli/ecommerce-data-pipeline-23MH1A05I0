INSERT INTO warehouse.fact_sales (
  date_key,
  customer_key,
  product_key,
  payment_method_key,
  transaction_id,
  quantity,
  unit_price,
  discount_amount,
  line_total,
  profit
)
SELECT
  d.date_key,
  c.customer_key,
  p.product_key,
  pm.payment_method_key,
  ti.transaction_id,
  ti.quantity,
  ti.price_at_time AS unit_price,
  0 AS discount_amount,
  ti.line_total,
  ti.line_total - (ti.price_at_time * ti.quantity * 0.30) AS profit
FROM production.transaction_items ti
JOIN production.transactions t
  ON ti.transaction_id = t.transaction_id
JOIN warehouse.dim_date d
  ON d.full_date = t.transaction_date
JOIN warehouse.dim_customers c
  ON c.customer_id = t.customer_id
 AND c.is_current = TRUE
JOIN warehouse.dim_products p
  ON p.product_id = ti.product_id
 AND p.is_current = TRUE
JOIN warehouse.dim_payment_method pm
  ON pm.payment_method_name = t.payment_method;
