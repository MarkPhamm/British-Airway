import logging
from typing import NoReturn

import extract
import data_cleaning
import feature_engineering

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_etl_pipeline() -> NoReturn:
    try:
        logging.info("Starting ETL pipeline")
        
        logging.info("Extracting data")
        extract.main()
        
        logging.info("Cleaning data")
        data_cleaning.main()
        
        logging.info("Performing feature engineering")
        feature_engineering.main()
        
        logging.info("ETL pipeline completed successfully")
    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {str(e)}")
        raise

if __name__ == "__main__":
    setup_logging()
    run_etl_pipeline()