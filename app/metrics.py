import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import app.utils as utils

def calculate_general_metrics(df):
    recommendation_percentage = round(df['recommended'].mean() * 100,2)  # Changed to round to remove decimals
    average_money_value = round(df['money_value'].mean(),2)
    average_service_score = round(df['score'].mean(),2)
    review_count = len(df)
    return recommendation_percentage, average_money_value, average_service_score, review_count

def filter_current_month(df):
    current_date = datetime.now()
    df['date_review'] = pd.to_datetime(df['date_review'])
    return df.loc[(df['date_review'].dt.month == current_date.month) & (df['date_review'].dt.year == current_date.year)]

def filter_previous_month(df):
    current_date = datetime.now()
    previous_month_first_day = current_date - relativedelta(months=1)
    previous_month_first_day = previous_month_first_day.replace(day=1)
    previous_month_last_day = previous_month_first_day + relativedelta(day=31)
    return df.loc[(df['date_review'] >= previous_month_first_day) & (df['date_review'] <= previous_month_last_day)]

def filter_previous_year_month(df):
    current_date = datetime.now()
    previous_year_first_day = current_date.replace(year=current_date.year - 1, month=current_date.month, day=1)
    previous_year_last_day = previous_year_first_day + relativedelta(day=31)
    return df.loc[(df['date_review'] >= previous_year_first_day) & (df['date_review'] <= previous_year_last_day)]

def calculate_metrics_for_month(df):
    recommendation_percentage = 0 if pd.isna(df['recommended'].mean()) else round(df['recommended'].mean() * 100, 2)
    average_money_value = 0 if pd.isna(df['money_value'].mean()) else round(df['money_value'].mean(), 2)
    average_service_score = 0 if pd.isna(df['score'].mean()) else round(df['score'].mean(), 2)
    review_count = len(df)
    return recommendation_percentage, average_money_value, average_service_score, review_count

def calculate_metrics(df, compare_with):
    recommendation_percentage, average_money_value, average_service_score, review_count = calculate_general_metrics(df)

    this_month_df = filter_current_month(df)
    
    if compare_with == 'previous month':
        previous_month_df = filter_previous_month(df)
        previous_metrics = calculate_metrics_for_month(previous_month_df)
    elif compare_with == 'previous year':
        previous_month_df = filter_previous_year_month(df)
        previous_metrics = calculate_metrics_for_month(previous_month_df)
    elif compare_with == 'all time':
        previous_metrics = (recommendation_percentage, average_money_value, average_service_score, review_count)
    else:
        previous_metrics = (0, 0, 0, 0)  # Default if no comparison is made

    this_recommendation_percentage, this_average_money_value, this_average_service_score, this_review_count = calculate_metrics_for_month(this_month_df)

    # Calculate changes in metrics
    change_recommendation_percentage = (this_recommendation_percentage - previous_metrics[0]) / previous_metrics[0] * 100 if previous_metrics[0] != 0 else 0
    change_average_money_value = (this_average_money_value - previous_metrics[1]) / previous_metrics[1] * 100 if previous_metrics[1] != 0 else 0
    change_average_service_score = (this_average_service_score - previous_metrics[2]) / previous_metrics[2] * 100 if previous_metrics[2] != 0 else 0
    change_review_count = this_review_count - previous_metrics[3]

    return (recommendation_percentage, average_money_value, average_service_score, review_count,
            this_recommendation_percentage, this_average_money_value, this_average_service_score, this_review_count,
            previous_metrics[0], previous_metrics[1], previous_metrics[2], previous_metrics[3],
            change_recommendation_percentage, change_average_money_value, change_average_service_score, change_review_count)

def display_metrics(df):
    # Display last refresh date
    utils.display_last_refresh_date()

    # Self-selection bias acknowledgement
    st.write("""
        **Self-Sampling Bias:**
        While analyzing reviews of British Airways, it's crucial to acknowledge the presence of self-selection sampling bias. Similar to social media platforms like Yelp, individuals who voluntarily submit reviews may have had extreme experiences, affiliations with the airline, or simply different motivations compared to those who do not provide feedback. Due to self-sampling bias, the KPI and review will be worse than the general population. However, it's important to clarify that our aim is not to generalize findings about the entire population. Instead, we focus on identifying specific areas for improvement that British Airways can address.
        """)
    compare_with = st.selectbox("Compare with:", ["previous month", "previous year", "all time"])
    
    metrics_data = calculate_metrics(df, compare_with)
    (recommendation_percentage, average_money_value, average_service_score, review_count,
     this_recommendation_percentage, this_average_money_value, this_average_service_score, this_review_count,
     previous_recommendation_percentage, previous_average_money_value, previous_average_service_score, previous_review_count,
     change_recommendation_percentage, change_average_money_value, change_average_service_score, change_review_count) = metrics_data

    # Display the percentages as a dashboard for this month
    current_date = datetime.now().date()
    st.header(F'This Month Metrics ({current_date.strftime("%B - %Y")})')
    col1, space1, col2, space2, col3, space3, col4 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1])
    with col1:
        st.metric(label="Recommendation Percentage", value=f"{this_recommendation_percentage}%",  # Removed decimal formatting
                   delta=f"{change_recommendation_percentage:.2f}% {compare_with}")
        st.caption('A higher percentage indicates customers are more likely to recommend.')
    with col2:
        st.metric(label="VFM Score", value=f"{this_average_money_value:.2f} / 5", delta=f"{change_average_money_value:.3f}% from last {compare_with}")
        st.caption('A higher score indicates greater satisfaction with the investment.')
    with col3:
        st.metric(label="Service Score", value=f"{this_average_service_score:.2f} / 5", delta=f"{change_average_service_score:.3f}% from last {compare_with}")
        st.caption('A higher score indicates greater satisfaction with services.')
    with col4:
        st.metric(label="Total number of reviews", value=f"{this_review_count:.0f}", delta=f"{change_review_count} reviews from last {compare_with}")
        st.caption('Total number of reviews from Air Quality.')

    show_comparison = st.checkbox("Show comparison metrics")
    if show_comparison:
        st.header(f'Comparison Metrics ({compare_with})')
        col1, space1, col2, space2, col3, space3, col4 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1])
        with col1:
            st.metric(label="Previous Recommendation Percentage", value=f"{previous_recommendation_percentage}%",  # Removed decimal formatting
            )
            st.caption('Comparison with the previous period.')
        with col2:
            st.metric(label="Previous VFM Score", value=f"{previous_average_money_value:.2f} / 5")
            st.caption('Comparison with the previous period.')
        with col3:
            st.metric(label="Previous Service Score", value=f"{previous_average_service_score:.2f} / 5")
            st.caption('Comparison with the previous period.')
        with col4:
            st.metric(label="Previous Total number of reviews", value=f"{previous_review_count:.0f}")
            st.caption('Comparison with the previous period.')
