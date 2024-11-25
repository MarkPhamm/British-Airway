import logging
import time
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config as cfg
from etl import extract, transform, load
from dagster import asset, Definitions, RunRequest, schedule, AssetSelection

start_time = time.time()

@asset
def run_etl_pipeline() -> None:
    try:
        logging.info("Starting ETL pipeline")

        cfg.last_refresh = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open('config.py', 'r') as config_file:
            lines = config_file.readlines()
        with open('config.py', 'w') as config_file:
            for line in lines:
                if 'last_refresh' not in line:
                    config_file.write(line)
            config_file.write(f"last_refresh = '{cfg.last_refresh}'\n")
        
        steps = [
            ("Extracting data", extract),
            ("Performing feature engineering", transform),
            ("Uploading data to S3", load)
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

@schedule(
    cron_schedule = "0 6 * * *", 
    target=AssetSelection.assets("run_etl_pipeline")
)

def daily_schedule():
    return RunRequest()

defs = Definitions(
    assets=[run_etl_pipeline],
    schedules=[daily_schedule]
)