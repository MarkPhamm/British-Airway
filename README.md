# British Airway Review (Phase 1)
**End-to-end Analytics Project for British Airway:** Analyze Customer Experience
This project will simulate a data team at British Airways, from ETL to Business Intelligence and Data Science. we will extract real-time data from [Air Inequality](https://www.airlinequality.com/airline-reviews/british-airways), and perform 4 types of modern analytics to find insightful recommendations.

![image](https://github.com/MarkPhamm/British-Airway/assets/99457952/919f1671-e640-4308-a908-8070585ded96)
## TL; DR:
**Problems:**

**Problem 1:**
- **Economy Customer Concerns:** Economy class customers prioritize staff services, while non-economy customers prioritize food and seat comfort.
  
![Problem 1](https://github.com/MarkPhamm/British-Airway/assets/99457952/fad27d46-f9c1-4187-94af-02da65d3f10b)

- **Specifics for Economy Class:**
  - Customers with negative staff experiences (staff score <= 2) predominantly travel through London (Heathrow and Gatwick) airports.
  - They are often solo or couple leisure travelers from the United Kingdom or the USA, suggesting they may require assistance with travel and navigating through airports.
                ![Problem 1 Details](https://github.com/MarkPhamm/British-Airway/assets/99457952/665ff202-218a-4862-a130-98ce4c8584b9)

**Solutions:**
- Enhance staff training programs to improve customer interactions and service quality.
- Increase staff presence and assistance at London airports, especially during peak travel times, to better support economy-class travelers.
- Implement feedback mechanisms for customers to report negative staff experiences promptly, allowing for swift resolution and continuous improvement.

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

## Project Flow Chart

## Project Steps
### 1. Extract - Transform - Load (ETL)
#### 1.1 Data Extraction (extract.py):
The `Extract.py` script scrapes real-time reviews from the British Airways page on the Airline Quality website using BeautifulSoup and requests. It iterates through specified pages, extracting review details like date, customer name, country, review body, and ratings on various aspects of the airline service. The extracted data is stored in a pandas DataFrame and saved to a CSV file named `raw_data.csv`.

#### 1.2 Data Cleaning (data_cleaning.py):
The `data_cleaning.py` script preprocesses data using pandas. It removes parentheses from country names, splits review bodies into 'review' and 'verified' columns, and parses date information. The script standardizes column names, reorders them, and saves the cleaned data to `clean_data.csv`.

#### 1.3 Feature Engineering and Transformation (feature_engineering.py)
The `clean_data.py` script preprocesses data for analysis. It calculates an overall score, cleans the 'route' column into 'origin', 'destination', and 'transit', splits aircraft types, standardizes names, and categorizes customer experience. It also converts 'Yes' and 'No' values to boolean and reorders columns. This script streamlines data cleaning and expansion, saving results to the `clean_data_expand.csv`.

### 2. Data Analysis
#### 2.1: Exploratory Data Analysis (EDA.ipynb)
Exploratory Data Analysis in Python
The EDA explored the British Airways flight dataset through data preprocessing, general analysis of null values and score distributions, service rating analysis with visualizations, sentiment analysis on reviews, and correlation heatmaps. It investigated poor ground experiences for economy class, highlighting issues at London/Heathrow. For non-economy, it focused on food and seat comfort, comparing ratings across segments like recommended/non-recommended flights. Time series analysis visualized score and review count trends over monthly/yearly periods. The analysis uncovered data quality insights, service performance factors, experience elements impacting ratings, and potential seasonal effects to guide further modeling efforts.
 
* Hypothesis: Economy type tends to care more about Staff, while non-economy care more about Food and Seat comfort
  * For economy class: Most customers travel through London, especially Heathrow and Gatwick, and most of the complaint about ground staff comes from this area. The top 2 most dominant problems with staff are their attitude and lack of staff presence.
  * For non-economy class: Seat and food are not up to expectations
 
#### 2.2: Review Analysis (review_analysis.ipynb)
Review/Sentiment Analysis in Python

### 3. Predictive Modelling and Feature Engineering
#### 3.1 Feature importance selection
The MoneyValueModel determines the top 3 most important factors that affect a customer's MoneyValue:
* Economy Type: Staff
* Non-Economy: Food, Seat comfort

This will further confirm our Hypothesis when doing EDA. 
#### 3.2 Classify London Staff Review 
In this model, we will use Natural Language Processing (NLP) to classify London Staff problems into 3 categories: Staff's attitude, Lack of Staff, and Others

### 4. Streamlit app building
Here's an overview dashboard app 
* [Review app](https://ba-review.streamlit.app/)
* Findings: Something wrong with BA in 2017 and 2023

### 5. Data Modelling and Power BI dashboard
Data Model: 

### Solution and Take Aways


# British Airway Booking (Phase 2)
We have received extra British Airways booking data (`booking_data.csv`) and will do further analysis on this







