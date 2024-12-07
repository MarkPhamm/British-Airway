import logging
from typing import NoReturn
import time
import os
import sys
import argparse
from datetime import datetime

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config as cfg
from etl import extract, transform, load

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def run_etl_pipeline(upload_to_s3: bool) -> NoReturn:
    start_time = time.time()
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
            ("Performing feature engineering", transform)
        ]
        
        if upload_to_s3:
            steps.append(("Uploading data to S3", load))
        
        for step, module in steps:
            logging.info(step)
            module.main()
        
        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"ETL pipeline completed successfully in {total_time:.2f} seconds")
    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Run ETL pipeline")
    parser.add_argument("--upload_to_s3", type=bool, default=True, help="Upload data to S3 (default: False)")
    args = parser.parse_args()

    setup_logging()
    run_etl_pipeline(args.upload_to_s3)

if __name__ == "__main__":
    main()
