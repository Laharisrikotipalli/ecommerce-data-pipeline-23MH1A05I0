import json
import os

REPORT_PATH = "data/processed/monitoring_report.json"

def test_quality_report_exists():
    assert os.path.exists(REPORT_PATH)


def test_quality_score_valid():
    with open(REPORT_PATH) as f:
        report = json.load(f)

    score = report["checks"]["data_quality"]["quality_score"]
    assert 0 <= score <= 100


def test_null_checks_detectable():
    with open(REPORT_PATH) as f:
        report = json.load(f)

    assert "null_violations" in report["checks"]["data_quality"]
