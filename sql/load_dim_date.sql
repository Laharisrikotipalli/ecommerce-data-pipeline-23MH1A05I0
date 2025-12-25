INSERT INTO warehouse.dim_date (
  date_key,
  full_date,
  year,
  quarter,
  month,
  day,
  month_name,
  day_name,
  week_of_year,
  is_weekend
)
SELECT
  TO_CHAR(d, 'YYYYMMDD')::INT AS date_key,
  d AS full_date,
  EXTRACT(YEAR FROM d),
  EXTRACT(QUARTER FROM d),
  EXTRACT(MONTH FROM d),
  EXTRACT(DAY FROM d),
  TO_CHAR(d, 'Month'),
  TO_CHAR(d, 'Day'),
  EXTRACT(WEEK FROM d),
  CASE WHEN EXTRACT(DOW FROM d) IN (0,6) THEN TRUE ELSE FALSE END
FROM generate_series(
  DATE '2024-01-01',
  DATE '2025-12-31',
  INTERVAL '1 day'
) d;
