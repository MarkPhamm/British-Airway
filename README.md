# British Airways Analytics Project

![British Airways Logo](https://github.com/MarkPhamm/British-Airway/assets/99457952/919f1671-e640-4308-a908-8070585ded96)

Access our Dashboard: [British Airways Dashboard](https://british-airways-dashboard-website.vercel.app/)

## 1. Project Overview
This end-to-end analytics project implements a modern data pipeline for British Airways, covering extraction, transformation, loading, and visualization of customer review data from [Air Inequality](https://www.airlinequality.com/airline-reviews/british-airways). The architecture leverages industry-standard tools and cloud services to create a robust, scalable analytics solution.

## 2. Architecture Overview
![BA Architecture](https://github.com/user-attachments/assets/d64c1a15-baa5-44a6-a086-49706aff2822)

### 2.1. Extraction Layer
- **Repository**: [british_airways_extract_load](https://github.com/vietlam2002/british_airways_extract_load)
- **Technology Stack**:
  - Python 3.12 with Pandas
  - Apache Airflow for workflow orchestration
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

### 2.2. Transformation Layer

- **Repository**: [british_airways_transformation](https://github.com/MarkPhamm/british_airways_transformation)
- **Technology Stack**:
  - dbt (data build tool)
  - Snowflake data warehouse
  - Apache Airflow with Astronomer
  - CI/CD via GitHub Actions

#### 2.2.1. Data Model
The project implements a dimensional star schema:

![Schema Diagram](https://github.com/user-attachments/assets/f6276b06-9f03-410a-b2cc-785b0a23b8f2)

- **Fact Table**: `fct_review` (one row per customer review per flight)
- **Dimension Tables**:
  - `dim_customer`: Identity and demographic information
  - `dim_aircraft`: Aircraft details and specifications
  - `dim_location`: Airport and city information
  - `dim_date`: Calendar and fiscal time tracking

#### 2.2.2. Transformation Process
1. Data loading into Snowflake staging area
2. Implementation of dbt models for dimensional modeling
3. Business logic application and metrics calculation
4. Data quality testing and validation

#### 2.2.3. CI/CD Pipeline
- Automated dbt runs via GitHub Actions
- Daily scheduled transformations
- Email notifications on completion/failure

### 2.3. Data Cleaning Layer

- **Repository**: [british_airways_data_cleaning](https://github.com/DucLe-2005/british_airways_data_cleaning)
- **Technology Stack**:
  - Python 3.12.5
  - Pandas for data manipulation
  - Regular expressions for text processing

#### 2.3.1. Data Cleaning Steps
1. Column standardization and renaming
2. Date formatting and standardization
3. Text cleaning and extraction
4. Route parsing and airport/city extraction
5. Aircraft name normalization
6. Rating conversion and typing

#### 2.3.2. Data Quality Assurance
- Null value handling
- Type consistency enforcement
- Format standardization
- Edge case management

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

### 3.1. Economy Customer Experience

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

### 3.2. Non-Economy Customer Experience

#### 3.2.1. Key Findings
- Non-economy customers prioritize food quality and seat comfort
- Business travelers expect premium service commensurate with pricing
- Complaints focus on cramped Business Class seating and poor food quality

#### 3.2.2. Recommended Solutions
- Redesign Business Class seating arrangement
- Elevate in-flight dining quality and presentation

## 4. Team Structure

### 4.1. Project Leadership
- **[Nhan Tran](https://www.linkedin.com/in/panicpotatoe/)**: Lead MLE at One Mount (Advisor)
- **[Mark Pham](https://www.linkedin.com/in/minhbphamm/)**: Mathematics & MIS at TCU (Team Leader)

### 4.2. Engineering Teams
- **Data Engineering**: [Leonard Dau](https://www.linkedin.com/in/leonard-dau-722399238/), [Thieu Nguyen](https://www.linkedin.com/in/thieunguyen1402/)
- **Data Analysis**: [Vy Nie](https://www.linkedin.com/in/vy-nie-712731227/), [Minh Ngo](https://www.linkedin.com/in/ngovoanhminh/), [Ahri Nguyen](https://www.linkedin.com/in/aringuyen26/)
- **BI & Visualization**: [Quan Tran](https://www.linkedin.com/in/hquantran/)
- **Data Science**: [Robin Tran](https://www.linkedin.com/in/robin-tran/)

## 5. Technical Documentation

### 5.1. ETL Pipeline Components

#### 5.1.1. Extract-Load Pipeline
The Extract-Load pipeline uses Apache Airflow DAGs to orchestrate:
- Web scraping tasks
- Data validation and initial cleaning
- S3 uploading operations
- Snowflake data loading

#### 5.1.2. dbt Transformation Pipeline
The dbt pipeline includes:
- Source definitions and staging models
- Dimensional modeling implementation
- Incremental loading strategy
- Data tests and documentation

#### 5.1.3. Data Cleaning Pipeline
The data cleaning process includes:
- Standardized column naming
- Date and text formatting
- Route parsing and extraction
- Rating normalization

### 5.2. Deployment Information
- Docker containerization for local development
- AWS cloud infrastructure for production
- Astronomer for Airflow management
- GitHub Actions for CI/CD automation
