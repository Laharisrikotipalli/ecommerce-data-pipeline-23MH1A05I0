# scripts/pipeline_orchestrator.py

import time
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path

# ==================================================
# Paths & Directories
# ==================================================
LOG_DIR = Path("logs")
REPORT_DIR = Path("data/processed")

LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now().strftime("%Y%m%d_%H%M%S")

MAIN_LOG_FILE = LOG_DIR / f"pipeline_orchestrator_{RUN_TS}.log"
ERROR_LOG_FILE = LOG_DIR / "pipeline_errors.log"

# ==================================================
# Logging Configuration
# ==================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(MAIN_LOG_FILE),
        logging.StreamHandler()
    ]
)

error_logger = logging.getLogger("pipeline_errors")
error_handler = logging.FileHandler(ERROR_LOG_FILE)
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

# ==================================================
# Custom Exception for Transient Errors
# ==================================================
class TransientError(Exception):
    """Retryable errors like DB timeout, network issue"""
    pass

# ==================================================
# Pipeline Step Implementations (Replace with real logic later)
# ==================================================
def data_generation():
    time.sleep(1)
    return 1000

def data_ingestion():
    time.sleep(1)
    return 1000

def data_quality_checks():
    time.sleep(1)
    return 995

def staging_to_production():
    time.sleep(1)
    return 995

def warehouse_load():
    time.sleep(1)
    return 995

def analytics_generation():
    time.sleep(1)
    return 5

# ==================================================
# Step Executor with Retry + Backoff
# ==================================================
def execute_step(step_name, step_function, max_retries=3):
    retries = 0
    start_time = time.time()

    while True:
        try:
            logging.info(f"START step: {step_name}")
            records = step_function()

            duration = round(time.time() - start_time, 2)

            logging.info(
                f"SUCCESS step: {step_name} | records={records} | duration={duration}s"
            )

            return {
                "status": "success",
                "duration_seconds": duration,
                "records_processed": records,
                "error_message": None,
                "retry_attempts": retries
            }

        except TransientError as te:
            retries += 1
            if retries > max_retries:
                logging.error(f"Max retries exceeded for {step_name}")
                raise

            backoff = 2 ** (retries - 1)
            logging.warning(
                f"Transient error in {step_name}. Retry {retries}/{max_retries} after {backoff}s"
            )
            time.sleep(backoff)

        except Exception as e:
            error_logger.error(
                f"FAILED step: {step_name}\n{traceback.format_exc()}"
            )
            raise

# ==================================================
# Main Pipeline Orchestrator
# ==================================================
def run_pipeline():
    pipeline_start_time = datetime.utcnow()
    pipeline_start_iso = pipeline_start_time.isoformat()

    report = {
        "pipeline_execution_id": f"PIPE_{RUN_TS}",
        "start_time": pipeline_start_iso,
        "end_time": None,
        "total_duration_seconds": None,
        "status": None,
        "steps_executed": {},
        "data_quality_summary": {
            "quality_score": 100,
            "critical_issues": 0
        },
        "errors": [],
        "warnings": []
    }

    steps = [
        ("data_generation", data_generation),
        ("data_ingestion", data_ingestion),
        ("data_quality_checks", data_quality_checks),
        ("staging_to_production", staging_to_production),
        ("warehouse_load", warehouse_load),
        ("analytics_generation", analytics_generation)
    ]

    try:
        for step_name, step_func in steps:
            result = execute_step(step_name, step_func)
            report["steps_executed"][step_name] = result

        report["status"] = "success"

    except Exception as e:
        report["status"] = "failed"
        report["errors"].append(str(e))
        logging.error("PIPELINE FAILED – Execution stopped")

    finally:
        pipeline_end_time = datetime.utcnow()
        report["end_time"] = pipeline_end_time.isoformat()

        # ✅ FIXED DURATION CALCULATION (NO ERROR)
        report["total_duration_seconds"] = round(
            (pipeline_end_time - pipeline_start_time).total_seconds(),
            2
        )

        report_path = REPORT_DIR / "pipeline_execution_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logging.info("Pipeline execution report generated successfully")
        logging.info(f"Report location: {report_path}")

# ==================================================
# Entry Point
# ==================================================
if __name__ == "__main__":
    run_pipeline()
