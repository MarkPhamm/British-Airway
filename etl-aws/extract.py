import os
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(number_of_pages: int) -> pd.DataFrame:
    base_url = "https://www.airlinequality.com/airline-reviews/british-airways"
    page_size = 100

    reviews_data = []

    for page in range(1, number_of_pages + 1):
        print(f"Scraping page {page}")

        url = f"{base_url}/page/{page}/?sortby=post_date%3ADesc&pagesize={page_size}"
        response = requests.get(url)
        response.raise_for_status()

        parsed_content = BeautifulSoup(response.content, 'html.parser')
        reviews = parsed_content.select('article[class*="comp_media-review-rated"]')

        for review in reviews:
            review_data = extract_review_data(review)
            reviews_data.append(review_data)

    df = pd.DataFrame(reviews_data)
    os.makedirs('data', exist_ok=True)
    df.to_csv("data/raw_data.csv", index=False)
    return df

def extract_review_data(review: BeautifulSoup) -> Dict[str, str]:
    review_data = {}

    review_data['dates'] = extract_text(review, "time", itemprop="datePublished")
    review_data['customer_names'] = extract_text(review, "span", itemprop="name")
    review_data['countries'] = extract_country(review)
    review_data['review_bodies'] = extract_text(review, "div", itemprop="reviewBody")

    extract_ratings(review, review_data)

    return review_data

def extract_text(element: BeautifulSoup, tag: str, **attrs) -> str:
    found = element.find(tag, attrs)
    return found.text.strip() if found else None

def extract_country(review: BeautifulSoup) -> str:
    country = review.find(string=lambda string: string and '(' in string and ')' in string)
    return country.strip('()') if country else None

def extract_ratings(review: BeautifulSoup, review_data: Dict[str, str]) -> None:
    review_ratings = review.find('table', class_='review-ratings')
    if not review_ratings:
        return

    for row in review_ratings.find_all('tr'):
        header = row.find('td', class_='review-rating-header')
        if not header:
            continue

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

def main():
    extract(40)

if __name__ == "__main__":
    main()