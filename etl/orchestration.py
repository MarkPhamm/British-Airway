import logging
import time
import os
import sys
from typing import NoReturn
from datetime import datetime
import argparse
from dagster import asset, Definitions, RunRequest, schedule, AssetSelection

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config as cfg
from etl import extract, transform, load

# Setup logging configuration
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Main ETL pipeline logic
@asset
def run_etl_pipeline() -> None:
    setup_logging()
    start_time = time.time()
    try:
        logging.info("Starting ETL pipeline")

        cfg.last_refresh = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update the last_refresh in the config file
        config_path = os.path.join(parent_dir, "config.py")
        with open(config_path, "r") as config_file:
            lines = config_file.readlines()
        with open(config_path, "w") as config_file:
            for line in lines:
                if "last_refresh" not in line:
                    config_file.write(line)
            config_file.write(f"last_refresh = '{cfg.last_refresh}'\n")

        steps = [
            ("Extracting data", extract),
            ("Performing feature engineering", transform),
            ("Uploading data to S3", load),
        ]

        for step, module in steps:
            logging.info(step)
            module.main()

        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"ETL pipeline completed successfully in {total_time:.2f} seconds")
    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {str(e)}")
        raise

# Schedule for the ETL pipeline
@schedule(
    cron_schedule="45 21 * * *",  # 3 PM CST
    target=AssetSelection.assets("run_etl_pipeline")
)
def daily_schedule():
    return RunRequest()

# Definitions for Dagster
defs = Definitions(
    assets=[run_etl_pipeline],
    schedules=[daily_schedule],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ETL pipeline")
    parser.add_argument("--upload_to_s3", type=bool, default=True, help="Upload data to S3 (default: True)")
    args = parser.parse_args()

    # Run the ETL pipeline
    run_etl_pipeline()
