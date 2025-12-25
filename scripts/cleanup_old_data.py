# scripts/cleanup_old_data.py

import yaml
import logging
from pathlib import Path
from datetime import datetime, timedelta

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config" / "config.yaml"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "scheduler_activity.log"

TARGET_DIRS = [
    BASE_DIR / "data" / "raw",
    BASE_DIR / "data" / "staging",
    BASE_DIR / "logs"
]

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)

# --------------------------------------------------
# Load config
# --------------------------------------------------
with open(CONFIG_FILE) as f:
    config = yaml.safe_load(f)

RETENTION_DAYS = config["retention"]["days"]
PRESERVE_KEYWORDS = config["retention"]["preserve_keywords"]

# --------------------------------------------------
# Cleanup Logic
# --------------------------------------------------
def should_preserve(file_path):
    name = file_path.name.lower()
    if any(keyword in name for keyword in PRESERVE_KEYWORDS):
        return True

    # Preserve today's files
    today = datetime.now().date()
    return datetime.fromtimestamp(file_path.stat().st_mtime).date() == today

def cleanup():
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    removed = 0

    for directory in TARGET_DIRS:
        if not directory.exists():
            continue

        for file in directory.glob("*"):
            if file.is_file():
                if file.stat().st_mtime < cutoff.timestamp():
                    if should_preserve(file):
                        continue

                    file.unlink()
                    removed += 1
                    logging.info(f"Deleted old file: {file}")

    logging.info(f"Cleanup completed. Files removed: {removed}")

# --------------------------------------------------
if __name__ == "__main__":
    cleanup()
