import streamlit as st
import pandas as pd
import app.data_processing as dp
import app.metrics as metrics
import app.visualization as vis
import app.utils as utils
from datetime import datetime
import config as cfg

import os
import sys
import warnings

import streamlit as st
from dotenv import load_dotenv

import config as cfg

# Load environment variables
load_dotenv('.env')
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

# Handle deployment configurations
if cfg.deploy:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    aws_access_key_id = st.secrets['aws_access_key_id']
    aws_secret_access_key = st.secrets['aws_secret_access_key']

import warnings

def display_dashboard(aws_access_key_id, aws_secret_access_key):
    # -----------------------------------------------------------
    if cfg.data_source == 's3':
        df = dp.read_df_from_s3(aws_access_key_id, aws_secret_access_key)
    else:
        df = dp.read_df_from_csv()

    df['date_review'] = pd.to_datetime(df['date_review']).dt.date
    # Slicers
    st.sidebar.title('General filters')
    verified_filter = st.sidebar.multiselect('Verified', df['verified'].dropna().unique(), default=None)
    recommended_filter = st.sidebar.multiselect('Recommended', df['recommended'].dropna().unique(), default=None)
    country_filter = st.sidebar.multiselect('Country', df['country'].dropna().unique())
    origin_filter = st.sidebar.multiselect('Origin', df['origin'].dropna().unique())
    destination_filter = st.sidebar.multiselect('Destination', df['destination'].dropna().unique())
    transit_filter = st.sidebar.multiselect('Transit', df['transit'].dropna().unique(), default=None)
    aircraft_1_filter = st.sidebar.multiselect('Aircraft 1', df['aircraft_1'].dropna().unique())
    aircraft_2_filter = st.sidebar.multiselect('Aircraft 2', df['aircraft_2'].dropna().unique())
    type_filter = st.sidebar.multiselect('Type', df['type'].dropna().unique())
    seat_type_filter = st.sidebar.multiselect('Seat Type', df['seat_type'].dropna().unique())
    experience_filter = st.sidebar.multiselect('Experience', df['experience'].dropna().unique())

    st.sidebar.title('Datetime Filters')
    month_review_filter = st.sidebar.multiselect('Month of Review', range(1, 13), default=list(range(1, 13)))
    year_review_filter = st.sidebar.multiselect('Year of Review', range(min(df['date_review']).year, max(df['date_review']).year + 1), default=list(range(min(df['date_review']).year, max(df['date_review']).year + 1)))

    def filter_data(df):
        # Filter the DataFrame
        if (verified_filter or recommended_filter or country_filter or origin_filter or destination_filter or transit_filter or aircraft_1_filter or aircraft_2_filter or type_filter or seat_type_filter or experience_filter or month_review_filter or year_review_filter):
            filtered_df = df[
                (df['verified'].isin(verified_filter) if verified_filter else True) &
                (df['recommended'].isin(recommended_filter) if recommended_filter else True) &
                (df['country'].isin(country_filter) if country_filter else True) &
                (df['origin'].isin(origin_filter) if origin_filter else True) &
                (df['destination'].isin(destination_filter) if destination_filter else True) &
                (df['transit'] == transit_filter if transit_filter else True) &
                (df['aircraft_1'].isin(aircraft_1_filter) if aircraft_1_filter else True) &
                (df['aircraft_2'].isin(aircraft_2_filter) if aircraft_2_filter else True) &
                (df['type'].isin(type_filter) if type_filter else True) &
                (df['seat_type'].isin(seat_type_filter) if seat_type_filter else True) &
                (df['experience'].isin(experience_filter) if experience_filter else True) &
                (df['month_review_num'].isin(month_review_filter) if month_review_filter else True) &
                (df['year_review'].isin(year_review_filter) if year_review_filter else True)
            ]
            return filtered_df
        else:
            return df
            
    df = filter_data(df)

    # Streamlit app
    st.title('Flight Reviews')

    # -------------------------------------
    # Metrics Breakdown
    # Calculate general metrics
    metrics.display_metrics(df)
    st.markdown("&nbsp;")

    # Display the reviews
    if st.checkbox('Show all reviews'):
        st.write(df)
    else:
        st.write("Top 5 most recent reviews")
        st.write(df.head(5))
    # Chart Breakdown
    st.title('📊 Chart Breakdown')  
    
    if st.checkbox('Create your own chart'):
        pyg_app = vis.get_pyg_app(df)
        pyg_app.explorer()

    # Experience Breakdown
    st.subheader('Experience Breakdown')

    breakdown_option = st.selectbox(
    "Select the category for breakdown:",
    options=['customer type', 'seat type']  
    )
    breakdown_column = 'type' if breakdown_option == 'customer type' else 'seat_type'

    # Experience breakdown
    fig1 = vis.plot_experience(df, breakdown_column, chart_type='distribution')
    fig2 = vis.plot_experience(df, breakdown_column, chart_type='composition')

    col1, space, col2 = st.columns([4,0.5, 2])
    with col1:
        st.plotly_chart(fig1, use_container_width=True, height=400, width=100)

    with col2:
        st.plotly_chart(fig2, use_container_width=True, height=400, width=100)

    # Recommendation breakdown
    fig3 = vis.plot_recommendation(df, breakdown_column, chart_type='distribution')
    fig4 = vis.plot_recommendation(df, breakdown_column, chart_type='composition')

    col1, space1, col2 = st.columns([4,0.5, 2])
    with col1:
        st.plotly_chart(fig3, use_container_width=True, height=400, width=50)
    with col2:
        st.plotly_chart(fig4, use_container_width=True, height=300, width=100)

    # Rating Scores Breakdown
    st.subheader("Rating Scores Breakdown")

    # Score histogram
    fig5 = vis.plot_score_histogram(df)
    st.plotly_chart(fig5, use_container_width=True)

    # Ratings boxplots
    rating_columns = ['seat_comfort', 'cabin_serv', 'food', 'ground_service', 'wifi']
    fig6 = vis.plot_rating_boxplots(df, rating_columns)
    st.plotly_chart(fig6, use_container_width=True, height=600, width=400)
    
    # Time Intelligence
    st.subheader('Time Intelligence')
    df['date_review'] = pd.to_datetime(df['date_review'])

    fig9 = vis.plot_dual_axis_metrics(df)
    st.plotly_chart(fig9, use_container_width=True)

    # Ratings by year
    service = st.selectbox('Select a service to plot:', ['seat_comfort', 'cabin_serv', 'food', 'ground_service', 'wifi'])
    fig10 = vis.plot_service_ratings(df, service)
    fig10.update_layout(height=600)
    st.plotly_chart(fig10, use_container_width=True, height=200, width=400)
    
    # Country distribution map
    fig11 = vis.plot_country_distribution(df, service)
    st.plotly_chart(fig11, use_container_width=True, height=600, width=400)

def main():
    st.set_page_config(layout="wide", page_title="British Airways Review Dashboard", page_icon="🛫")
    display_dashboard(aws_access_key_id, aws_secret_access_key)

if __name__ == "__main__":
    main()
