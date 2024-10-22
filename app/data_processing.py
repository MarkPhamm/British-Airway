import pandas as pd
import boto3
from io import StringIO

# Function to get the most recent CSV file
def get_recent_csv_file(bucket_name, s3_client):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.csv'):
            return obj['Key']  # Return the most recent CSV file key

# Function to read a CSV file from S3 into a DataFrame
def read_csv_to_df(bucket_name, s3_client, file_key):
    csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    return df

def read_df_from_s3(aws_access_key_id, aws_secret_access_key):
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Name of the S3 bucket
    bucket_name = 'new-british-airline'

    # Get the most recent CSV file
    recent_csv_file = get_recent_csv_file(bucket_name, s3_client)

    # Read the file into a DataFrame
    return read_csv_to_df(bucket_name, s3_client, recent_csv_file) if recent_csv_file else None  # Return None if no file was read

def read_df_from_csv():
    df = pd.read_csv("data/processed_data.csv")
    return df

