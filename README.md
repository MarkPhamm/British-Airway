# British Airway Project
**End-to-end Analytics Project for British Airway:** Analyze Customer Experience
In the project, we will extract real-time data from [Air Inequality](https://www.airlinequality.com/airline-reviews/british-airways), and perform 4 types of modern analytics. With the goal of finding insightful recommendations, the team is divided into 4 main teams: Data Engineering (DE), Data Analytics (DA), Business Intelligence (BI), and Data Science (DS)

![image](https://github.com/MarkPhamm/British-Airway/assets/99457952/919f1671-e640-4308-a908-8070585ded96)

## Team members

* **Advisor/Mentor:** Offers guidance and oversight for the project.
  * [Nhan Tran](https://www.linkedin.com/in/panicpotatoe/): Lead MLE at One Mount

* **Team Leader/Analytics Engineer/BI Engineer:** Oversees the entire project, contributing to both technical and non-technical aspects.
  * [Mark Pham](https://www.linkedin.com/in/minhbphamm/): Mathematics & MIS at TCU

* **DE Team:** Responsible for extracting and transforming real-time data, and creating ETL pipelines using AWS services.
  * [Leonard Dau](https://www.linkedin.com/in/leonard-dau-722399238/): Computer Science at TCU
  * [Thieu Nguyen](https://www.linkedin.com/in/thieunguyen1402/): Computer Science at USF

* **DA Team:** Conducts metrics exploration, and documentation, discovers business insights, and provides client-facing recommendations.
  * [Vy Nie](https://www.linkedin.com/in/vy-nie-712731227/): Business Administration at FTU Vietnam
  * [Minh Ngo](https://www.linkedin.com/in/ngovoanhminh/): Business Administration at FTU Vietnam
  * [Ahri Nguyen](https://www.linkedin.com/in/aringuyen26/?fbclid=IwAR2k9TjhUZ8QiMywx5VoBI1QWri5Q3g8dgjYwUk6N9iHMVSSZFSn0n42QGg): Business Administration at FTU Vietnam

* **BI Team:** Builds Power BI dashboards to generate insights and recommendations.
  * [Quan Tran](https://www.linkedin.com/in/hquantran/): Economics & Business Analytics at USF

* **DS Team:** Develops predictive models and analyzes the importance of different features.
  * [Robin Tran](https://www.linkedin.com/in/robin-tran/): Data Science at Mount Holyoke College

## Project Life cycle

![image](https://github.com/MarkPhamm/British-Airway/assets/99457952/aeff38f4-f999-4905-849a-68afe1514190)

## Project Steps

### Data Extraction (Extraction.py):
The Extract.py script utilizes BeautifulSoup and requests to scrape real-time reviews from the British Airways page on the Airline Quality website. It iterates through a specified number of pages, extracting review details such as date, customer name, country, review body, and ratings on various aspects of the airline service. The extracted data is stored in a pandas DataFrame and saved to a CSV file named 'raw_data.csv'.
and saves it to a CSV file named 'raw_data.csv'.

### Data Cleaning (Data Cleaning.py):
The Extract.py script imports pandas as pd and numpy as np libraries to clean and organize data obtained from a CSV file named 'raw_data.csv'.


### Streamlit app building
Here's an overview app of the data
1. [Review app](https://ba-review.streamlit.app/)
2. [Booking app](https://ba-booking.streamlit.app/)




