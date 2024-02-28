
from bs4 import BeautifulSoup
import requests
import pandas as pd

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


    df = pd.DataFrame(reviews_data) 
    df.to_csv("raw_data.csv")

if __name__ == "__main__":
    main()