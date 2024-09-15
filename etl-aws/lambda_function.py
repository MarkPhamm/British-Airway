import json

from bs4 import BeautifulSoup
import pandas as pd
import os 

import data_cleaning
import feature_engineering

from datetime import datetime
import io

import boto3
import requests

def main():
    base_url = "https://www.airlinequality.com/airline-reviews/british-airways"
    pages = 100
    page_size = 100

    reviews_data = []

    for i in range(1, pages + 1): 

        print(f"Scraping page {i}")

        # Create URL to collect links from paginated data
        url = f"{base_url}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"

        # Collect HTML data from this page
        response = requests.get(url)

        # Parse content
        content = response.content
        parsed_content = BeautifulSoup(content, 'html.parser')

        # Extracting reviews
        reviews = parsed_content.select('article[class*="comp_media-review-rated"]')

        # Extracting review details
        for review in reviews:
            review_data = {}

            # Extract the date tag
            date_tag = review.find("time", itemprop="datePublished")
            if date_tag:
                review_data['dates'] = date_tag.text.strip()

            # Extracting customer names
            customer_name_tag = review.find("span", itemprop="name")
            if customer_name_tag:
                review_data['customer_names'] = customer_name_tag.text.strip()

            # Extracting country
            country = review.find(text=lambda text: text and '(' in text and ')' in text)
            if country:
                country = country.strip('()')
            else:
                country = None

            review_data['countries'] = country

            # Extracting review bodies
            review_body = review.find("div", itemprop="reviewBody")
            if review_body:
                review_data['review_bodies'] = review_body.text.strip()

            # Extracting review ratings
            review_ratings = review.find('table', class_='review-ratings')
            if review_ratings:
                rows = review_ratings.find_all('tr')
                for row in rows:
                    header = row.find('td', class_='review-rating-header')
                    if header:
                        header_text = header.text.strip()
                        if header_text in ['Seat Comfort', 'Cabin Staff Service', 'Food & Beverages', 'Ground Service', 'Wifi & Connectivity', 'Value For Money']:
                            stars_td = row.find('td', class_='review-rating-stars')
                            if stars_td:
                                stars = stars_td.find_all('span', class_='star fill')
                                review_data[header_text] = len(stars)
                        else:
                            value = row.find('td', class_='review-value')
                            if value:
                                review_data[header_text] = value.text.strip()

            # Append the review data dictionary to the reviews_data list
            reviews_data.append(review_data)

    print("Reviews Data:")
    for review_data in reviews_data:
        print(review_data)
        
        
    # cleaning
    df = pd.DataFrame(reviews_data)
    cleaned_df = data_cleaning.main()    

    # feature engineering
    engineered_df = feature_engineering.main()
    
    # upload to S3
    
    # S3 Bucket details
    bucket_name = 'british-airway'  # Replace with your S3 bucket name
    directory = "dataset"  # S3 directory
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"raw_data_{current_date}.csv"  # File will be named like 'raw_data_2023-04-01.csv'
    s3_file_path = f"{directory}/{filename}"
    
    # Using boto3 to access S3
    s3 = boto3.client('s3')
    
    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    engineered_df.to_csv(csv_buffer, index=False)
    
    # Upload to S3
    s3.put_object(Bucket=bucket_name, Key=s3_file_path, Body=csv_buffer.getvalue())
    print(f"File uploaded successfully to {s3_file_path} in bucket {bucket_name}")
    


def lambda_handler(event, context):
    # TODO implement
    main()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
