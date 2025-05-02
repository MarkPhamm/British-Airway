# British Airways Analytics Project

![British Airways Logo](https://github.com/MarkPhamm/British-Airway/assets/99457952/919f1671-e640-4308-a908-8070585ded96)

Access our Dashboard: [British Airways Dashboard](https://british-airways-dashboard-website.vercel.app/)

## Team Structure

### Project Leadership
- **Mentor/Stakeholder**: [Nhan Tran](https://www.linkedin.com/in/panicpotatoe/) - Lead MLE at One Mount
- **Analytics Engineer - Team Lead**: [Mark Pham](https://www.linkedin.com/in/minhbphamm/) - Mathematics & MIS at TCU

### Engineering Teams
- **Data Engineering**: [Leonard Dau](https://www.linkedin.com/in/leonard-dau-722399238/), [Thieu Nguyen](https://www.linkedin.com/in/thieunguyen1402/)
- **Software Engineer**: [Tien Nguyen](https://www.linkedin.com/in/tien-nguyen-598758329), [Anh Duc Le](https://www.linkedin.com/in/duc-le-517420205/)
- **Data Scientist**: [Robin Tran](https://www.linkedin.com/in/robin-tran/)
- **Scrum Master**: [Hien Dinh](https://www.linkedin.com/in/hiendinhq)

## 1. Project Overview
This end-to-end analytics project implements a modern data pipeline for British Airways, covering extraction, transformation, loading, and visualization of customer review data from [Air Inequality](https://www.airlinequality.com/airline-reviews/british-airways). The architecture leverages industry-standard tools and cloud services to create a robust, scalable analytics solution.


**Self-selection bias:** While analyzing reviews of British Airways, it's crucial to acknowledge the presence of self-selection sampling bias. Similar to social media platforms like Yelp, individuals who voluntarily submit reviews may have had extreme experiences, affiliations with the airline, or simply different motivations compared to those who do not provide feedback. Due to self-sampling bias, the KPI and review will be worse than the general population. However, it's important to clarify that our aim is not to generalize findings about the entire population. Instead, we focus on identifying specific areas for improvement that British Airways can address.

## 2. Architecture Overview
![BritishAirways](https://github.com/user-attachments/assets/2a9d45e6-be1b-4582-a9a0-3b7fb7536d9f)

### 2.1. Extraction Layer
- **Repository**: [british_airways_extract_load](https://github.com/vietlam2002/british_airways_extract_load)
- **Technology Stack**:
  - Python 3.12 with Pandas
  - Apache Airflow 
for workflow orchestration
  - AWS S3 for data lake storage
  - Docker for containerization

#### 2.1.1. Data Source
The pipeline extracts customer review data from [AirlineQuality.com](https://www.airlinequality.com/airline-reviews/british-airways), which provides detailed information about flight experiences.

#### 2.1.2. Extraction Process
1. Web crawling using BeautifulSoup and requests
2. Initial data capture and formatting
3. Storage of raw data as CSV files
4. Orchestration via Apache Airflow DAGs

#### 2.1.3. AWS Integration
- S3 buckets for raw data storage
- IAM roles and permissions management
- Error logging and monitoring

### 2.2. Data Cleaning Layer

- **Repository**: [british_airways_data_cleaning](https://github.com/DucLe-2005/british_airways_data_cleaning)
- **Technology Stack**:
  - Python 3.12.5
  - Pandas for data manipulation
  - Regular expressions for text processing

#### 2.2.1. Data Cleaning Steps
1. Column standardization and renaming
2. Date formatting and standardization
3. Text cleaning and extraction
4. Route parsing and airport/city extraction
5. Aircraft name normalization
6. Rating conversion and typing

#### 2.2.2. Data Quality Assurance
- Null value handling
- Type consistency enforcement
- Format standardization
- Edge case management

### 2.3. Transformation Layer

- **Repository**: [british_airways_transformation](https://github.com/MarkPhamm/british_airways_transformation)
- **Technology Stack**:
  - dbt (data build tool)
  - Snowflake data warehouse
  - Apache Airflow with Astronomer
  - CI/CD via GitHub Actions

#### 2.3.1. Data Model
The project implements a dimensional star schema:

![Schema Diagram](https://github.com/user-attachments/assets/f6276b06-9f03-410a-b2cc-785b0a23b8f2)

- **Fact Table**: `fct_review` (one row per customer review per flight)
- **Dimension Tables**:
  - `dim_customer`: Identity and demographic information
  - `dim_aircraft`: Aircraft details and specifications
  - `dim_location`: Airport and city information
  - `dim_date`: Calendar and fiscal time tracking

#### 2.3.2. Transformation Process
1. Data loading into Snowflake staging area
2. Implementation of dbt models for dimensional modeling
3. Business logic application and metrics calculation
4. Data quality testing and validation

#### 2.3.3. CI/CD Pipeline
- Automated dbt runs via GitHub Actions
- Daily scheduled transformations
- Email notifications on completion/failure

### 2.4. Visualization Layer

- **Repository**: [british_airways_dashboard_website](https://github.com/nguyentienTCU/british_airways_dashboard_website)
- **Dashboard**: [Live Dashboard](https://british-airways-dashboard-website.vercel.app/)

#### 2.4.1. Front-End Implementation
- Interactive dashboards with filtering capabilities
- Comprehensive KPI tracking
- Temporal analysis visualization
- Customer segment comparison tools

#### 2.4.2. Advanced Analytics Integration
- RAG Chatbot powered by LangChain and Chroma DB
- Sentiment analysis visualization
- Feature importance modeling results

## 3. Key Business Insights

### 3.1. Economic Customer Experience

![Problem 1](https://github.com/MarkPhamm/British-Airway/assets/99457952/fad27d46-f9c1-4187-94af-02da65d3f10b)

#### 3.1.1. Key Findings
- Economy class customers prioritize staff services
- Negative experiences concentrated at London airports (Heathrow and Gatwick)
- 95% of complaints relate to insufficient ground staff support and staff attitude

![Problem 1 Details](https://github.com/MarkPhamm/British-Airway/assets/99457952/665ff202-218a-4862-a130-98ce4c8584b9)

#### 3.1.2. Recommended Solutions
- Enhance staff training programs
- Increase staff presence at London airports
- Implement prompt feedback mechanisms

### 3.2. Non-Economic Customer Experience

#### 3.2.1. Key Findings
- Non-economy customers prioritize food quality and seat comfort
- Business travelers expect premium service commensurate with pricing
- Complaints focus on cramped Business Class seating and poor food quality

#### 3.2.2. Recommended Solutions
- Redesign Business Class seating arrangement
- Elevate in-flight dining quality and presentation
