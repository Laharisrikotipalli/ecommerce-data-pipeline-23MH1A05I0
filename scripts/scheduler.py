# scripts/scheduler.py

import subprocess
import time
import yaml
import logging
from datetime import datetime
from pathlib import Path
import schedule
import sys
import os

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = CONFIG_FILE = BASE_DIR / "config" / "config.yaml"

LOCK_FILE = BASE_DIR / "pipeline.lock"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

SCHEDULER_LOG = LOG_DIR / "scheduler_activity.log"

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(SCHEDULER_LOG),
        logging.StreamHandler()
    ]
)

# --------------------------------------------------
# Load config
# --------------------------------------------------
with open(CONFIG_FILE) as f:
    config = yaml.safe_load(f)

RUN_TIME = config["scheduler"]["run_time"]
PREVENT_CONCURRENT = config["scheduler"]["prevent_concurrent"]

# --------------------------------------------------
# Lock Handling (Concurrency Prevention)
# --------------------------------------------------
def is_pipeline_running():
    return LOCK_FILE.exists()

def create_lock():
    LOCK_FILE.write_text(str(os.getpid()))

def remove_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()

# --------------------------------------------------
# Pipeline Runner
# --------------------------------------------------
def run_pipeline():
    if PREVENT_CONCURRENT and is_pipeline_running():
        logging.warning("Pipeline already running. Skipping execution.")
        return

    try:
        logging.info("Scheduler triggered pipeline execution")
        create_lock()

        result = subprocess.run(
            [sys.executable, "scripts/pipeline_orchestrator.py"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logging.info("Pipeline execution SUCCESS")
            subprocess.run(
                [sys.executable, "scripts/cleanup_old_data.py"],
                cwd=BASE_DIR
            )
        else:
            logging.error("Pipeline execution FAILED")
            logging.error(result.stderr)

    except Exception as e:
        logging.error(f"Scheduler failure: {str(e)}")

    finally:
        remove_lock()

# --------------------------------------------------
# Scheduler Setup
# --------------------------------------------------
schedule.every().day.at(RUN_TIME).do(run_pipeline)

logging.info(f"Scheduler started. Pipeline scheduled daily at {RUN_TIME}")

# --------------------------------------------------
# Scheduler Loop
# --------------------------------------------------
try:
    while True:
        schedule.run_pending()
        time.sleep(30)
except KeyboardInterrupt:
    logging.info("Scheduler stopped manually")
