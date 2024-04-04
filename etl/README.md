# Airline Quality ETL Pipeline

## Introduction

This repository contains the implementation of an Extract, Transform, Load (ETL) pipeline that periodically scrapes customer reviews for British Airways from AirlineQuality.com. The data is processed and used for analytical and machine learning purposes. The pipeline is designed within the AWS Cloud environment, leveraging a combination of AWS Lambda, AWS S3, and Amazon Athena for robust, scalable, and efficient data handling.

## Pipeline Overview

The ETL pipeline is scheduled to run weekly to ensure the analysis is performed on up-to-date data. It consists of three main processes, each handled by a separate Python script:

1. `lambda_function.py` - Orchestrates the scraping, invoking of data cleaning, and feature engineering scripts.
2. `data_cleaning.py` - Cleans the raw scraped data by handling missing values, removing duplicates, and normalizing text.
3. `feature_engineering.py` - Transforms the clean data into a format suitable for analysis and machine learning, creating features that will feed into predictive models.

## Why This Pipeline?

The purpose of this ETL pipeline is to automate the collection and preprocessing of valuable airline customer feedback data. Analyzing customer reviews can reveal insights into overall customer satisfaction, service quality, and areas needing improvement. By scheduling the pipeline to run weekly, we can track changes in customer sentiment over time, allowing for timely data-driven decisions.

## Usage

The pipeline is designed to be triggered on a weekly basis, but can be manually invoked if needed. Below are the steps to set up and run the pipeline:

1. Configure AWS Lambda with the `lambda_function.py` to initiate the ETL process.
2. Ensure `data_cleaning.py` and `feature_engineering.py` are available in the Lambda environment or in an S3 bucket for Lambda to access.
3. Set up the required IAM roles and permissions for Lambda to access S3 and run Athena queries.
4. Monitor the pipeline runs and outputs in the designated S3 bucket and through Amazon CloudWatch logs.

## AWS Cloud Components

- **AWS Lambda**: Manages the orchestration of the ETL tasks.
- **Amazon S3**: Serves as the storage for the raw data, intermediate files, and the final processed datasets.
- **Amazon Athena**: Used for running SQL queries on the data stored in S3, facilitating easy data analysis and integration with other AWS services for machine learning.

## Conclusion

This ETL pipeline is a critical component in understanding customer feedback and driving improvements in service quality for British Airways. The weekly schedule ensures a constant influx of fresh data, enabling ongoing monitoring and analysis.

For any issues or contributions to this pipeline, please feel free to open an issue or a pull request.

