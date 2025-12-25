
-- Query 1: Data Freshness
SELECT
    'staging' AS layer,
    MAX(loaded_at) AS latest_record,
    EXTRACT(EPOCH FROM (NOW() - MAX(loaded_at))) / 3600 AS hours_since_update
FROM staging.orders

UNION ALL

SELECT
    'production',
    MAX(created_at),
    EXTRACT(EPOCH FROM (NOW() - MAX(created_at))) / 3600
FROM production.orders

UNION ALL

SELECT
    'warehouse',
    MAX(created_at),
    EXTRACT(EPOCH FROM (NOW() - MAX(created_at))) / 3600
FROM warehouse.fact_sales;


-- Query 2: Volume Trend (30 days)

WITH daily_counts AS (
    SELECT
        DATE(created_at) AS day,
        COUNT(*) AS record_count
    FROM warehouse.fact_sales
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY 1
)
SELECT
    AVG(record_count) AS mean_count,
    STDDEV(record_count) AS std_dev,
    MIN(record_count) AS min_count,
    MAX(record_count) AS max_count
FROM daily_counts;

-- Query 3: Today's Volume

SELECT COUNT(*) AS today_count
FROM warehouse.fact_sales
WHERE DATE(created_at) = CURRENT_DATE;


-- Query 4: Data Quality Checks

-- Orphan records
SELECT COUNT(*) AS orphan_records
FROM warehouse.fact_sales f
LEFT JOIN warehouse.dim_customers c
ON f.customer_key = c.customer_key
WHERE c.customer_key IS NULL;


-- Null violations
SELECT COUNT(*) AS null_violations
FROM warehouse.fact_sales
WHERE product_key IS NULL OR customer_key IS NULL;


-- Query 5: Pipeline Execution History

SELECT
    MAX(executed_at) AS last_run,
    COUNT(*) FILTER (WHERE status = 'failed') AS failures,
    AVG(duration_seconds) AS avg_duration
FROM monitoring.pipeline_runs
WHERE executed_at >= NOW() - INTERVAL '7 days';


-- Query 6: Database Health

SELECT
    COUNT(*) AS active_connections
FROM pg_stat_activity;
