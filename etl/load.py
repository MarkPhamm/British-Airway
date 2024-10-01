import logging
from typing import NoReturn
import pandas as pd
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime
import io
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_to_s3(df: pd.DataFrame, bucket_name: str, directory: str) -> None:
    """
    Upload a DataFrame to S3 as a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to upload.
        bucket_name (str): The name of the S3 bucket.
        directory (str): The directory within the bucket to store the file.

    Raises:
        BotoCoreError: If there's an error with the AWS SDK.
        ClientError: If there's an error with the S3 client operation.
    """
    s3_client = boto3.client('s3')
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"processed_data_{current_date}.csv"
    s3_file_path = f"{directory}/{filename}"

    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_file_path,
            Body=csv_buffer.getvalue()
        )
        logging.info(f"File uploaded successfully to s3://{bucket_name}/{s3_file_path}")
    except (BotoCoreError, ClientError) as e:
        logging.error(f"Failed to upload file to S3: {str(e)}")
        raise

def main() -> None:
    """
    Main function to run the S3 upload process.

    Reads the processed data and uploads it to S3.
    """
    try:
        data_dir = Path("data")
        input_file = data_dir / "processed_data.csv"
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        df = pd.read_csv(input_file)
        bucket_name = 'new-british-airline'
        s3_directory = "dataset"
        upload_to_s3(df, bucket_name, s3_directory)
    except Exception as e:
        logging.error(f"An error occurred in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()