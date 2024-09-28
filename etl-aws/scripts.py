import logging
from typing import NoReturn
import time

import extract
import data_cleaning
import feature_engineering

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_etl_pipeline() -> NoReturn:
    start_time = time.time()
    try:
        logging.info("Starting ETL pipeline")
        
        logging.info("Extracting data")
        extract.main()
        
        logging.info("Cleaning data")
        data_cleaning.main()
        
        logging.info("Performing feature engineering")
        feature_engineering.main()
        
        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"ETL pipeline completed successfully in {total_time:.2f} seconds")
    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {str(e)}")
        raise

if __name__ == "__main__":
    setup_logging()
    run_etl_pipeline()