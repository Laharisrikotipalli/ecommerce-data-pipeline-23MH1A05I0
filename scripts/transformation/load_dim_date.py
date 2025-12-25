from datetime import date, timedelta
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://admin:password@localhost:5433/ecommerce_db"
)

def load_dim_date():
    start = date(2024, 1, 1)
    end = date(2024, 12, 31)

    rows = []
    d = start
    while d <= end:
        rows.append({
            "date_key": int(d.strftime("%Y%m%d")),
            "full_date": d,
            "year": d.year,
            "quarter": (d.month - 1) // 3 + 1,
            "month": d.month,
            "day": d.day,
            "month_name": d.strftime("%B"),
            "day_name": d.strftime("%A"),
            "week_of_year": d.isocalendar()[1],
            "is_weekend": d.weekday() >= 5
        })
        d += timedelta(days=1)

    df = pd.DataFrame(rows)
    df.to_sql("dim_date", engine, schema="warehouse", if_exists="append", index=False)

    print("✅ dim_date loaded (366 rows)")

if __name__ == "__main__":
    load_dim_date()
