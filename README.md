# British Airway Review (Phase 1)
* Access the Streamlit website dashboard [here](https://ba-review.streamlit.app/)

**End-to-end Analytics Project for British Airway:** Analyze Customer Experience
This project will simulate a data team at British Airways, from ETL to Business Intelligence and Data Science. we will extract real-time data from [Air Inequality](https://www.airlinequality.com/airline-reviews/british-airways), and perform 4 types of modern analytics to find insightful recommendations.

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

## About the data

### Data Source
[Air Inequality](https://www.airlinequality.com/airline-reviews/british-airways) is a robust platform for assessing British Airways' service quality through diverse customer reviews and ratings. Providing insights into cabin comfort, amenities, and overall satisfaction, enables customers to share feedback. However, the data's reliance on customer surveys may introduce bias.

### Self-Sampling Bias Acknowledge
**Self-Sampling bias:** The reviews of restaurants, hotels, cafes, and so on that you read on social media sites like Yelp are prone to bias because the people submitting them are not randomly selected; rather, they themselves have taken the initiative to write. This leads to self-selection bias — the people motivated to write reviews may be those who had poor experiences, may have an association with the establishment, or may simply be a different type of person from those who do not write reviews. Note that while self-selection samples can be unreliable indicators of the true state of affairs, they may be more reliable in simply comparing one establishment to a similar one; the same self-selection bias might apply to each.

While analyzing reviews of British Airways, it's crucial to acknowledge the presence of self-selection sampling bias. Similar to social media platforms like Yelp, individuals who voluntarily submit reviews may have had extreme experiences, affiliations with the airline, or simply different motivations compared to those who do not provide feedback. Due to Self-sampling, bias, the KPI and review will be worse than the population. However, it's important to clarify that our aim is not to generalize findings about the entire population. Instead, we focus on identifying specific areas for improvement that British Airways can address.

### Cleaned Data
- `Id`: Order of each review, where smaller numbers represent later reviews. (Ordinal, Int)
- `Date review`: The date when the review was conducted. (Ordinal, Date)
- `Day review`: The day of the week when the review was conducted. (Discrete, Int)
- `Month review`: The month when the review was conducted. (Ordinal, String)
- `Month review num`: The numerical representation of the month when the review was conducted. (Discrete, Int)
- `Year review`: The year when the review was conducted. (Discrete, Int)
- `Verified`: Indicates whether the review was successfully verified or not. (Nominal, Boolean)
- `Name`: Name of the passenger who provided the review. (Nominal, String)
- `Month fly`: The month of the flight date. (Ordinal, String)
- `Month fly num`: The numerical representation of the month of the flight date. (Discrete, Int)
- `Year fly`: The year of the flight date. (Discrete, Int)
- `Month year fly`: The month and year of the flight date. (Ordinal, Date)
- `Country`: Nationality of the passenger. (Nominal, String)
- `Aircraft`: Type of the airplane used for the flight. (Nominal, String)
- `Type`: Purpose of the flight (e.g., business, leisure). (Nominal, String)
- `Seat Type`: Class of the seat (e.g., Economy, Business). (Ordinal, String)
- `Origin`: Departure location of the passenger. (Nominal, String)
- `Destination`: Final destination of the passenger. (Nominal, String)
- `Transit`: Location where the passenger was transited. (Nominal, String)
- `Seat Comfort`: Passenger’s evaluation of seat comfort on a scale of 1 to 5. (Ordinal, Int)
- `Cabin service`: Passenger’s evaluation of the cabin service on a scale of 1 to 5. (Ordinal, Int)
- `Ground service`: Passenger’s evaluation of the ground service on a scale of 1 to 5. (Ordinal, Int)
- `Wifi`: Passenger’s evaluation of the on-board wifi connection on a scale of 1 to 5. (Ordinal, Int)
- `Money value`: Passenger's evaluation of how the flight experience corresponds to the money paid on a scale of 1 to 5. (Ordinal, Int)
- `Score`: Average of the scores given by the passenger on seat comfort, cabin service, ground service, wifi, and money value. (Continuous, Float)
- `Experience`: Overall rating of the flight experience categorized into poor, fair, and good. (Ordinal, String)
- `Recommended`: Indicates whether the passenger would recommend the same flight experience. (Nominal, Boolean)
- `Review`: Detailed feedback provided by the passenger regarding their flight experience. (Nominal, String)

# Business Problems, Solutions, and Takeaways
## Problems:

### Problem 1:
- **Economy Customer Concerns:** Economy class customers prioritize staff services, while non-economy customers prioritize food and seat comfort.
![Problem 1](https://github.com/MarkPhamm/British-Airway/assets/99457952/fad27d46-f9c1-4187-94af-02da65d3f10b)

#### Economy Class Drill Down:
  Customers with negative staff experiences (staff score <= 2) have the following traits:
  - Predominantly travel through London (Heathrow and Gatwick) airports.
  - They are often solo or couple leisure travelers from the United Kingdom or the USA, suggesting they may require assistance with travel and navigating through airports.
                ![Problem 1 Details](https://github.com/MarkPhamm/British-Airway/assets/99457952/665ff202-218a-4862-a130-98ce4c8584b9)
  - 95% of the problems related to the customer not receiving enough help from the ground staff (Due to lack of staff) and complaining about the staff's attitude/unprofessionalism

#### Solutions for problem 1:
- Enhance staff training programs to improve customer interactions and service quality.
- Increase staff presence and assistance at London airports, especially during peak travel times, to better support economy-class travelers.
- Implement feedback mechanisms for customers to report negative staff experiences promptly, allowing for swift resolution and continuous improvement.


### Problem 2 

**Non-Economy Customer Concerns**: While Economy class customers prioritize staff services, non-economy customers prioritize food and seat comfort.

#### Non-Economy Class Drill Down:**
  Customers with negative food and seat comfort experience (food score or seat comfort score <= 2) have the following traits:
  - Predominantly travel through London (Heathrow and Gatwick) airports.
  - They are often experienced business travelers who have high expectations with the airlines
  - They expected more from the service since they have paid more.
  - Mostly complain about the seat layout in the Business Class (cramped feeling due to the seating arrangement) and food (The food served on the flight was limited in choice, poorly presented, and lacked quality, with one passenger even describing it as if it had fallen on the floor and been scooped back onto the plate.)

#### Solutions for problem 2:**
- **Revamp Seat Layout:** Implement a redesigned seating arrangement in Business Class that provides more space and comfort, alleviating the cramped feeling often complained about by customers.
- **Enhance In-flight Dining Experience:** Elevate the quality and presentation of food offerings, ensuring a wider selection, better presentation, and higher quality ingredients to meet the expectations of experienced business travelers who have paid a premium for their service.
 

## Project Flow Chart

## Project Steps
### 1. Extract - Transform - Load (ETL) - Airline Quality ETL Pipeline

This repository contains the implementation of an Extract, Transform, Load (ETL) pipeline that periodically scrapes customer reviews for British Airways from AirlineQuality.com. The data is processed and used for analytical and machine-learning purposes. The pipeline is designed within the AWS Cloud environment, leveraging a combination of AWS Lambda, AWS S3, and Amazon Athena for robust, scalable, and efficient data handling.

![image](https://github.com/MarkPhamm/British-Airway/assets/88282475/cb0d9a6d-5c10-4754-b88a-5ace9474cb09)

#### 1.1 Data Extraction (extract.py):
The `Extract.py` script scrapes real-time reviews from the British Airways page on the Airline Quality website using BeautifulSoup and requests. It iterates through specified pages, extracting review details like date, customer name, country, review body, and ratings on various aspects of the airline service. The extracted data is stored in a pandas DataFrame and saved to a CSV file named `raw_data.csv`.

#### 1.2 Data Cleaning (data_cleaning.py):
The `data_cleaning.py` script preprocesses data using pandas. It removes parentheses from country names, splits review bodies into 'review' and 'verified' columns, and parses date information. The script standardizes column names, reorders them, and saves the cleaned data to `clean_data.csv`.

#### 1.3 Feature Engineering and Transformation (feature_engineering.py)
The `clean_data.py` script preprocesses data for analysis. It calculates an overall score, cleans the 'route' column into 'origin', 'destination', and 'transit', splits aircraft types, standardizes names, and categorizes customer experience. It also converts 'Yes' and 'No' values to boolean and reorders columns. This script streamlines data cleaning and expansion, saving results to the `clean_data_expand.csv`.

#### 1.4 Why This Pipeline?
The purpose of this ETL pipeline is to automate the collection and preprocessing of valuable airline customer feedback data. Analyzing customer reviews can reveal insights into overall customer satisfaction, service quality, and areas needing improvement. By scheduling the pipeline to run weekly, we can track changes in customer sentiment over time, allowing for timely data-driven decisions.

#### 1.5 Usage
The pipeline is designed to be triggered on a weekly basis, but can be manually invoked if needed. Below are the steps to set up and run the pipeline:
1. Configure AWS Lambda with the `lambda_function.py` to initiate the ETL process.
2. Ensure `data_cleaning.py` and `feature_engineering.py` are available in the Lambda environment or in an S3 bucket for Lambda to access.
3. Set up the required IAM roles and permissions for Lambda to access S3 and run Athena queries.
4. Monitor the pipeline runs and outputs in the designated S3 bucket and through Amazon CloudWatch logs.

#### 1.6 AWS Cloud Components

- **AWS Lambda**: Manages the orchestration of the ETL tasks.
- **Amazon S3**: Serves as the storage for the raw data, intermediate files, and the final processed datasets.
- **Amazon Athena**: Used for running SQL queries on the data stored in S3, facilitating easy data analysis and integration with other AWS services for machine learning.

#### 1.7 Issues Encountered: Library Imports in AWS Lambda
One of the challenges we faced during the development of this pipeline was importing external libraries in AWS Lambda. Lambda provides a clean, isolated environment to run code, which makes it secure and efficient, but it also means that it does not have access to external libraries by default.

#### 1.8 Conclusion

This ETL pipeline is a critical component in understanding customer feedback and driving improvements in service quality for British Airways. The weekly schedule ensures a constant influx of fresh data, enabling ongoing monitoring and analysis.

For any issues or contributions to this pipeline, please feel free to open an issue or a pull request.



### 2. Data Analysis
#### 2.1: Exploratory Data Analysis (EDA.ipynb)
The `EDA.ipynb` file explored the British Airways flight dataset through data preprocessing, general analysis of null values and score distributions, service rating analysis with visualizations, sentiment analysis on reviews, and correlation heatmaps. It investigated poor ground experiences for economy class, highlighting issues at London/Heathrow. For non-economy, it focused on food and seat comfort, comparing ratings across segments like recommended/non-recommended flights. Time series analysis visualized score and review count trends over monthly/yearly periods. The analysis uncovered data quality insights, service performance factors, experience elements impacting ratings, and potential seasonal effects to guide further modeling efforts.
 
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

### 4. Streamlight app building
Here's an overview dashboard app 
* [Review app](https://ba-review.streamlit.app/)
* Findings: Something wrong with BA in 2017 and 2023

### 5. Data Modelling and Power BI dashboard
Data Model: 


# British Airway Booking (Phase 2)
We have received extra British Airways booking data (`booking_data.csv`) and will do further analysis on this







