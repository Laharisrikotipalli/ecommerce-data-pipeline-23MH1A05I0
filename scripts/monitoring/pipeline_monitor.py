import json
import psycopg2
import os
from datetime import datetime
from decimal import Decimal   # ✅ FIX 1

# =========================================================
# DATABASE CONFIG
# =========================================================
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "ecommerce_db",
    "user": "admin",
    "password": "password"   # must match docker POSTGRES_PASSWORD
}

# =========================================================
# SAFE ABSOLUTE PATH FOR REPORT
# =========================================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
REPORT_PATH = os.path.join(BASE_DIR, "data", "processed", "monitoring_report.json")
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

# =========================================================
# JSON SAFE SERIALIZER  ✅ FIX 2
# =========================================================
def json_safe(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# =========================================================
# HELPERS
# =========================================================
def fetch_one(cursor, query):
    cursor.execute(query)
    return cursor.fetchone()

def fetch_all(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

# =========================================================
# MAIN
# =========================================================
def main():
    alerts = []
    now = datetime.utcnow()
    now_iso = now.isoformat()

    # ---------------- CONNECT ----------------
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # =====================================================
    # 1. PIPELINE EXECUTION HEALTH
    # =====================================================
    last_run, failures, avg_duration = fetch_one(cur, """
        SELECT 
            MAX(executed_at),
            COUNT(*) FILTER (WHERE status = 'failed'),
            AVG(duration_seconds)
        FROM monitoring.pipeline_runs
        WHERE executed_at >= NOW() - INTERVAL '7 days'
    """)

    if last_run:
        hours_since_last = (now - last_run).total_seconds() / 3600
        pipeline_status = "ok"

        if hours_since_last > 25:
            pipeline_status = "critical"
            alerts.append({
                "severity": "critical",
                "check": "pipeline_execution",
                "message": "Pipeline has not run in over 25 hours",
                "timestamp": now_iso
            })
    else:
        hours_since_last = None
        pipeline_status = "critical"
        alerts.append({
            "severity": "critical",
            "check": "pipeline_execution",
            "message": "No pipeline execution history found",
            "timestamp": now_iso
        })

    # =====================================================
    # 2. DATA FRESHNESS
    # =====================================================
    freshness = fetch_all(cur, """
        SELECT layer, latest_record, hours_since_update
        FROM (
            SELECT 
                'staging' AS layer,
                MAX(loaded_at) AS latest_record,
                EXTRACT(EPOCH FROM (NOW() - MAX(loaded_at))) / 3600
                    AS hours_since_update
            FROM staging.transactions

            UNION ALL

            SELECT 
                'production' AS layer,
                MAX(created_at) AS latest_record,
                EXTRACT(EPOCH FROM (NOW() - MAX(created_at))) / 3600
                    AS hours_since_update
            FROM production.transactions

            UNION ALL

            SELECT 
                'warehouse' AS layer,
                MAX(created_at) AS latest_record,
                EXTRACT(EPOCH FROM (NOW() - MAX(created_at))) / 3600
                    AS hours_since_update
            FROM warehouse.fact_sales
        ) t
    """)

    max_lag = max(row[2] for row in freshness if row[2] is not None)
    freshness_status = "ok" if max_lag <= 24 else "critical"

    if freshness_status == "critical":
        alerts.append({
            "severity": "critical",
            "check": "data_freshness",
            "message": f"Data lag exceeded threshold: {round(max_lag, 2)} hours",
            "timestamp": now_iso
        })

    # =====================================================
    # 3. DATA VOLUME ANOMALY (SAFE STDDEV)
    # =====================================================
    mean, std_dev, _, _ = fetch_one(cur, """
        WITH daily AS (
            SELECT DATE(created_at) AS day, COUNT(*) AS cnt
            FROM warehouse.fact_sales
            WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY 1
        )
        SELECT AVG(cnt), STDDEV(cnt), MIN(cnt), MAX(cnt) FROM daily
    """)

    today_count = fetch_one(cur, """
        SELECT COUNT(*)
        FROM warehouse.fact_sales
        WHERE DATE(created_at) = CURRENT_DATE
    """)[0]

    anomaly = False
    anomaly_type = None
    expected_range = None

    if mean is not None and std_dev not in (None, 0):
        lower = mean - (3 * std_dev)
        upper = mean + (3 * std_dev)
        expected_range = f"{int(lower)}–{int(upper)}"

        if today_count > upper:
            anomaly = True
            anomaly_type = "spike"
        elif today_count < lower:
            anomaly = True
            anomaly_type = "drop"

    if anomaly:
        alerts.append({
            "severity": "warning",
            "check": "data_volume",
            "message": f"Volume anomaly detected ({anomaly_type})",
            "timestamp": now_iso
        })

    # =====================================================
    # 4. DATA QUALITY
    # =====================================================
    orphan_records = fetch_one(cur, """
        SELECT COUNT(*)
        FROM warehouse.fact_sales f
        LEFT JOIN warehouse.dim_customers c
        ON f.customer_key = c.customer_key
        WHERE c.customer_key IS NULL
    """)[0]

    null_violations = fetch_one(cur, """
        SELECT COUNT(*)
        FROM warehouse.fact_sales
        WHERE customer_key IS NULL OR product_key IS NULL
    """)[0]

    quality_score = max(0, 100 - (orphan_records + null_violations))
    quality_status = "ok" if quality_score >= 95 else "degraded"

    if quality_status == "degraded":
        alerts.append({
            "severity": "warning",
            "check": "data_quality",
            "message": f"Data quality score dropped to {quality_score}",
            "timestamp": now_iso
        })

    # =====================================================
    # 5. DATABASE HEALTH
    # =====================================================
    start = datetime.utcnow()
    cur.execute("SELECT 1")
    response_time_ms = (datetime.utcnow() - start).total_seconds() * 1000

    connections = fetch_one(cur, "SELECT COUNT(*) FROM pg_stat_activity")[0]

    # =====================================================
    # FINAL REPORT
    # =====================================================
    report = {
        "monitoring_timestamp": now_iso,
        "pipeline_health": pipeline_status,
        "checks": {
            "last_execution": {
                "status": pipeline_status,
                "last_run": last_run.isoformat() if last_run else None,
                "hours_since_last_run": hours_since_last,
                "threshold_hours": 25
            },
            "data_freshness": {
                "status": freshness_status,
                "max_lag_hours": round(max_lag, 2)
            },
            "data_volume_anomalies": {
                "status": "anomaly_detected" if anomaly else "ok",
                "actual_count": today_count,
                "expected_range": expected_range,
                "anomaly_type": anomaly_type
            },
            "data_quality": {
                "status": quality_status,
                "quality_score": quality_score,
                "orphan_records": orphan_records,
                "null_violations": null_violations
            },
            "database_connectivity": {
                "status": "ok",
                "response_time_ms": round(response_time_ms, 2),
                "connections_active": connections
            }
        },
        "alerts": alerts,
        "overall_health_score": quality_score
    }

    print("Writing monitoring report to:", REPORT_PATH)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2, default=json_safe)  # ✅ FIX 3

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
