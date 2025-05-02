# British Airways Analytics Project

![British Airways Logo](https://github.com/MarkPhamm/British-Airway/assets/99457952/919f1671-e640-4308-a908-8070585ded96)

Access our Dashboard: [British Airways Dashboard](https://british-airways-dashboard-website.vercel.app/)

## Repositories

- [british_airways_data_cleaning](https://github.com/DucLe-2005/british_airways_data_cleaning) — Owner: DucLe-2005  
  Cleans raw scraped data and standardizes formats using modular Python functions.

- [british_airways_extract_load](https://github.com/vietlam2002/british_airways_extract_load) — Owner: vietlam2002  
  Scrapes customer reviews, stages in S3, then loads them to Snowflake via Airflow-compatible ETL scripts.

- [british_airways_transformation](https://github.com/MarkPhamm/british_airways_transformation) — Owner: MarkPhamm  
  Handles dbt-based data transformation on Snowflake with CI/CD workflows via GitHub Actions.

- [british_airways_dashboard_website](https://github.com/nguyentienTCU/british_airways_dashboard_website) — Owner: nguyentienTCU  
  A dashboard website for visualizing insights from processed airline reviews.

- [bristish_airways_analysis](https://github.com/trungdam512/bristish_airways_analysis) — Owner: trungdam512  
  Focuses on EDA, ML models, and Sentiment Analysis.

## Team Structure

### Project Leadership
- **Mentor - Stakeholder**: [Nhan Tran](https://www.linkedin.com/in/panicpotatoe/)
- **Analytics Engineer - Team Lead**: [Mark Pham](https://www.linkedin.com/in/minhbphamm/)

### Engineering Teams
- **Data Engineering**: [Leonard Dau](https://www.linkedin.com/in/leonard-dau-722399238/), [Thieu Nguyen](https://www.linkedin.com/in/thieunguyen1402/), [Viet Lam Nguyen](https://www.linkedin.com/in/lam-nguyen-viet-051a57305)
- **Software Engineer**: [Tien Nguyen](https://www.linkedin.com/in/tien-nguyen-598758329), [Anh Duc Le](https://www.linkedin.com/in/duc-le-517420205/), 
- **Data Scientist**: [Robin Tran](https://www.linkedin.com/in/robin-tran/), [Trung Dam](https://www.linkedin.com/in/trung-dam-86962a235/)
- **Scrum Master**: [Hien Dinh](https://www.linkedin.com/in/hiendinhq)

## 1. Project Overview
This end-to-end analytics project implements a modern data pipeline for British Airways, covering extraction, transformation, loading, and visualization of customer review data from [Air Inequality](https://www.airlinequality.com/airline-reviews/british-airways). The architecture leverages industry-standard tools and cloud services to create a robust, scalable analytics solution.


**Self-selection bias:** While analyzing reviews of British Airways, it's crucial to acknowledge the presence of self-selection sampling bias. Similar to social media platforms like Yelp, individuals who voluntarily submit reviews may have had extreme experiences, affiliations with the airline, or simply different motivations compared to those who do not provide feedback. Due to self-sampling bias, the KPI and review will be worse than the general population. However, it's important to clarify that our aim is not to generalize findings about the entire population. Instead, we focus on identifying specific areas for improvement that British Airways can address.

## 2. Architecture Overview
![BritishAirways](https://github.com/user-attachments/assets/2a9d45e6-be1b-4582-a9a0-3b7fb7536d9f)

### 2.1. Extraction Layer

#### Overview
The extraction layer for the British Airways data pipeline handles the acquisition of customer review data from [AirlineQuality.com](https://www.airlinequality.com/airline-reviews/british-airways/). This module is responsible for scraping raw review data, storing it appropriately, and preparing it for subsequent processing stages.

- **Repository**: [british_airways_extract_load](https://github.com/vietlam2002/british_airways_extract_load)

#### 2.1.1. Technology Stack
- **Python 3.12 with Pandas**: Core data processing and manipulation
- **Apache Airflow**: Workflow orchestration and scheduling
- **AWS S3**: Data lake storage for both raw and processed data
- **Docker**: Containerization for consistent development and deployment
- **Snowflake**: Target data warehouse for storing processed data

#### 2.1.2. Data Source
The primary data source is [AirlineQuality.com](https://www.airlinequality.com/airline-reviews/british-airways/), which provides:
- Customer ratings
- Detailed review text
- Flight information
- Customer metadata
- Service quality assessments

#### 2.1.3. Extraction Process

##### Web Scraping Implementation
The extraction process begins with the `scrape_british_data` task in the Airflow DAG, which executes a Python script to:
1. Connect to AirlineQuality.com
2. Navigate through review pages
3. Extract structured data from HTML content
4. Compile results into a raw dataset

```python
# From main_dag.py - Extract task definition
scrape_british_data = BashOperator(
    task_id="scrape_british_data",
    bash_command="chmod -R 777 /opt/***/data && python /opt/airflow/tasks/scraper_extract/scraper.py"
)
```

##### Data Storage
- Raw data is initially stored as `raw_data.csv` in the project's data directory
- After successful extraction, a notification task confirms completion:

```python
note = BashOperator(
    task_id="note",
    bash_command="echo 'Succesfull extract data to raw_data.csv'"
)
```

#### 2.1.4. Data Cleaning & Initial Transformation
Following extraction, the data undergoes initial cleaning:

```python
clean_data = BashOperator(
    task_id='clean_data',
    bash_command="python /opt/airflow/tasks/transform/transform.py"
)
```

The cleaning process:
- Standardizes formats
- Handles missing values
- Removes duplicates
- Ensures data type consistency
- Prepares data for staging

#### 2.1.5. AWS S3 Integration

##### S3 Bucket Configuration
The cleaned data is uploaded to AWS S3 for staging:

```python
upload_cleaned_data_to_s3 = BashOperator(
    task_id='upload_cleaned_data_to_s3',
    bash_command="chmod -R 777 /opt/airflow/data && python /opt/airflow/tasks/upload_to_s3.py"
)
```

##### Security & Access Control
- IAM roles and permissions are configured to restrict access
- Encrypted transmission to ensure data security
- Versioning enabled to maintain audit trail

#### 2.1.6. Workflow Orchestration
The entire extraction process is orchestrated via Apache Airflow:

```python
with DAG(
    dag_id="british_pipeline",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1
) as dag:
    # Task definitions here
```

##### DAG Configuration
- **Schedule**: Daily execution (`timedelta(days=1)`)
- **Retry Logic**: Configured to retry failed tasks after 5 minutes
- **Dependencies**: Tasks are chained to ensure proper execution order

##### Task Dependencies
The extraction portion of the pipeline follows this sequence:
```
scrape_british_data >> note >> clean_data >> note_clean_data >> upload_cleaned_data_to_s3
```

#### 2.1.7. Snowflake Integration
After staging in S3, data is loaded to Snowflake:

```python
snowflake_copy_operator = BashOperator(
    task_id='snowflake_copy_from_s3',
    bash_command="pip install snowflake-connector-python python-dotenv && python /opt/airflow/tasks/snowflake_load.py"
)
```

##### Loading Strategy
- Uses Snowflake's COPY command for efficient data loading
- Configures column mapping and data type conversion
- Implements error handling and validation

### 2.2. Data Cleaning Layer

This layer transforms raw British Airways customer review data into a standardized, analysis-ready format.

#### 2.2.1. Project Overview

- **Repository**: [british_airways_data_cleaning](https://github.com/DucLe-2005/british_airways_data_cleaning)
- **Technology Stack**: Python 3.12.5 with Pandas, NumPy, Matplotlib, and Seaborn

#### 2.2.2. Data Cleaning Steps

##### 2.2.2.1. Column Standardization
- Converts column names to snake_case
- Standardizes special characters and naming conventions
- Renames specific columns for clarity (e.g., "country" → "nationality")

##### 2.2.2.2. Date Formatting
- Standardizes dates to ISO 8601 format ("YYYY-MM-DD")
- Handles both submission dates and flight dates
- Example: "19th March 2025" → "2025-03-19"

##### 2.2.2.3. Text Cleaning
- Extracts verification status from review text
- Creates boolean "verify" column
- Removes verification prefix from review content
- Cleans nationality field (e.g., "United Kingdom (UK)" → "United Kingdom")

##### 2.2.2.4. Route Processing
- Parses route information into structured components:
  - Origin city and airport
  - Destination city and airport
  - Transit points (if applicable)
- Handles both direct and connecting flight formats

##### 2.2.2.5. Aircraft Standardization
- Normalizes aircraft naming conventions
- Standardizes Boeing and Airbus nomenclature
- Example: "Aircraft: B777-300" → "Boeing 777-300"

##### 2.2.2.6. Rating Conversion
- Converts all rating fields to numeric format
- Uses Int64 data type to properly handle missing values
- Standardizes rating scales across all categories

#### 2.2.3. Data Quality Assurance

- **Null Value Handling**: Preserves legitimate nulls while ensuring consistent types
- **Type Consistency**: Enforces appropriate data types for each column
- **Format Standardization**: Ensures consistent formats for dates, aircraft names, and locations
- **Edge Case Management**: Handles various non-standard inputs and formats

#### 2.2.4. Output Schema

The cleaned dataset includes standardized fields for:
- Customer information (name, nationality)
- Review metadata (submission date, verification status)
- Flight details (aircraft, route, date flown, traveler type)
- Ratings across multiple service categories
- Derived fields (origin/destination cities and airports)

#### 2.2.5. Pipeline Integration

- **Input**: Receives raw data from extraction layer
- **Processing**: Triggered by Airflow DAG task `clean_data`
- **Output**: Produces cleaned data for S3 upload and subsequent Snowflake loading

### 2.3. Transformation Layer

This layer implements a dimensional modeling approach to transform cleaned British Airways customer review data into analytics-ready structures.

#### 2.3.1. Project Overview

- **Repository**: [british_airways_transformation](https://github.com/MarkPhamm/british_airways_transformation)
- **Technology Stack**:
  - dbt (data build tool) for transformations
  - Snowflake as the data warehouse
  - Apache Airflow with Astronomer for orchestration
  - GitHub Actions for CI/CD automation

#### 2.3.2. Data Model

The project implements a dimensional star schema:

![Schema Diagram](https://github.com/user-attachments/assets/f6276b06-9f03-410a-b2cc-785b0a23b8f2)

##### 2.3.2.1. Fact Table
- **`fct_review`**: Core fact table with one row per customer review per flight
  - Contains quantitative metrics (ratings)
  - Boolean indicators (verified, recommended)
  - Foreign keys to dimension tables

##### 2.3.2.2. Dimension Tables
- **`dim_customer`**: Customer identity and demographic information
- **`dim_aircraft`**: Aircraft details including manufacturer and model
- **`dim_location`**: Airport and city information for origin, destination, and transit points
- **`dim_date`**: Calendar and fiscal date tracking for both submission and flight dates

#### 2.3.3. Transformation Process

##### 2.3.3.1. Data Flow
1. Source data ingestion from cleaned dataset in Snowflake
2. Staging models to prepare data for dimensional modeling
3. Core dimension table creation and enrichment
4. Fact table construction with foreign key relationships
5. Final views and aggregations for business users

##### 2.3.3.2. dbt Implementation
- Models organized in layers (staging → dimensions → facts → reporting)
- Incremental loading strategy for efficiency
- Documentation and tests integrated into models
- Version control with Git

#### 2.3.4. Data Quality Framework

- **Schema Tests**: Column constraints, uniqueness, relationships
- **Custom Tests**: Business logic validation
- **Freshness Checks**: Data recency monitoring
- **Completeness Validation**: Coverage of expected data points

#### 2.3.5. CI/CD Pipeline

- **Triggers**:
  - Code pushes to main branch
  - Pull requests
  - Scheduled runs at 00:00 UTC every Monday
  - Manual execution option

- **Workflow Steps**:
  1. Environment setup with Python 3.12
  2. Dependencies installation
  3. dbt model execution against Snowflake
  4. Status notifications via email

- **Pipeline Status**: Tracked via GitHub Actions badges

#### 2.3.6. Integration Points

- **Upstream**: Receives data from data cleaning layer via Snowflake
- **Downstream**: Produces analytics-ready dimensional tables for BI tools
- **Orchestration**: Executed as part of the overall data pipeline via Airflow

--- 

### 2.4. Visualization Layer

This layer delivers interactive visualizations and analytical insights derived from the transformed British Airways customer review data.

#### 2.4.1. Project Overview

- **Repository**: [british_airways_dashboard_website](https://github.com/nguyentienTCU/british_airways_dashboard_website)
- **Live Dashboard**: [British Airways Analytics Dashboard](https://british-airways-dashboard-website.vercel.app/)
- **Technology Stack**:
  - Next.js for frontend framework
  - TailwindCSS for styling
  - Chart.js for data visualization
  - LangChain for RAG implementation
  - ChromaDB for vector database storage

#### 2.4.2. Front-End Implementation

##### 2.4.2.1. Dashboard Structure
- **Interactive KPI Cards**: Real-time metrics and performance indicators
- **Multi-dimensional Filtering**: Analysis by route, aircraft type, and customer segment
- **Responsive Design**: Mobile and desktop optimized interface
- **Data Explorer**: Custom query builder for ad-hoc analysis

##### 2.4.2.2. Visualization Components
- **Time Series Analysis**: Time series charts for tracking rating trends
- **Aircraft Analysis**: Aircraft model performance analysis
- **Route Analysis**: Route map with performance overlays

#### 2.4.3. Advanced Analytics Integration

##### 2.4.3.1. Natural Language Capabilities
- **RAG Chatbot**: LangChain-powered question answering system
- **Query Interface**: Natural language processing for data exploration
- **Context-Aware Responses**: Leveraging ChromaDB for semantic retrieval

##### 2.4.3.2. Analytical Models
- **Sentiment Analysis**: Visual representation of review sentiment
- **Feature Importance**: Key drivers of customer satisfaction

#### 2.4.4. Key Dashboard Features

- **Executive Summary**: High-level overview of performance metrics
- **Service Quality Tracker**: Detailed breakdown of rating categories
- **Customer Segment Analysis**: Demographic and preference-based insights
- **Aircraft Performance Comparison**: Rating variations across fleet types
- **Route Analysis**: Performance metrics by origin-destination pairs
- **Temporal Patterns**: Seasonal and trend-based visualizations

#### 2.4.5. Integration Points

- **Data Source**: Connects to transformed data in Snowflake
- **API Layer**: RESTful endpoints for dynamic data retrieval

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
