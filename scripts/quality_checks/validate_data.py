import pandas as pd
from sqlalchemy import create_engine, text
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def run_quality_checks():
    engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    
    # Standardized Report Schema
    report = {
        "check_timestamp": datetime.now().isoformat(),
        "checks_performed": {},
        "overall_quality_score": 0,
        "quality_grade": ""
    }

    with engine.connect() as conn:
        # Example: Referential Integrity Check
        orphan_sql = "SELECT count(*) FROM staging.transactions t LEFT JOIN staging.customers c ON t.customer_id = c.customer_id WHERE c.customer_id IS NULL"
        orphan_count = conn.execute(text(orphan_sql)).scalar()
        
        report["checks_performed"]["referential_integrity"] = {
            "status": "passed" if orphan_count == 0 else "failed",
            "orphan_records": orphan_count,
            "details": {"relationship": "transactions -> customers", "count": orphan_count}
        }

    # Scoring Methodology: 100 - (violations/total * weight)
    # For now, let's assume a perfect score if orphan_count is 0
    report["overall_quality_score"] = 100 if orphan_count == 0 else 70
    report["quality_grade"] = "A" if report["overall_quality_score"] >= 90 else "C"

    # Save to mandatory location
    os.makedirs('data/quality_reports', exist_ok=True)
    with open('data/quality_reports/quality_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    print("✓ Quality Report generated in data/quality_reports/quality_report.json")

if __name__ == "__main__":
    run_quality_checks()