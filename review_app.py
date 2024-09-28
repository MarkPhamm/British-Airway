import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta
import warnings

warnings.filterwarnings("ignore")

# Constants
COLOR_MAP_EXPERIENCE = {
    'Poor': '#e63946',
    'Fair': '#f4a261',
    'Good': '#2a9d8f'
}

COLOR_MAP_RECOMMENDATION = {
    True: '#2a9d8f',
    False: '#e63946'
}

# Helper functions
def create_chart(data, x, y, color, title, color_map=None, chart_type='bar'):
    if chart_type == 'bar':
        fig = px.bar(data, x=x, y=y, color=color, title=title, color_discrete_map=color_map)
    elif chart_type == 'pie':
        fig = go.Figure(data=[go.Pie(labels=data.index, values=data.values, hole=0.5, marker_colors=[color_map[x] for x in data.index])])
    
    fig.update_layout(title_text=title, showlegend=True)
    return fig

def create_histogram(data, title):
    fig = go.Figure(data=[go.Histogram(x=data, nbinsx=20, histnorm='probability density')])
    fig.update_layout(title=title, xaxis_title='Score', yaxis_title='Density')
    return fig

def create_box_plot(df, columns, title):
    fig = go.Figure()
    for col in columns:
        fig.add_trace(go.Box(y=df[col], name=col))
    fig.update_layout(title_text=title, yaxis=dict(title='Ratings', tickmode='array', tickvals=list(range(1, 6))))
    return fig

def create_line_plot(data, x, y, title):
    fig = px.line(data, x=x, y=y, title=title)
    fig.update_xaxes(title=x.capitalize())
    fig.update_yaxes(title=y.capitalize())
    return fig

# Main functions
def filter_data(df, filters):
    for column, values in filters.items():
        if values:
            df = df[df[column].isin(values)]
    return df

def calculate_metrics(df):
    metrics = {
        'recommendation_percentage': df['recommended'].mean() * 100,
        'average_money_value': df['money_value'].mean(),
        'average_service_score': df['score'].mean(),
        'review_count': len(df)
    }
    return metrics

def display_metrics(metrics, label):
    st.header(f'{label} Metrics')
    cols = st.columns(4)
    for i, (key, value) in enumerate(metrics.items()):
        with cols[i]:
            st.metric(label=key.replace('_', ' ').title(), value=f"{value:.2f}")

def main():
    st.set_page_config(layout="wide")
    
    df = pd.read_csv("data/processed_data.csv")
    df['date_review'] = pd.to_datetime(df['date_review'])

    # Filters
    filters = {
        'verified': st.sidebar.multiselect('Verified', df['verified'].dropna().unique()),
        'recommended': st.sidebar.multiselect('Recommended', df['recommended'].dropna().unique()),
        'country': st.sidebar.multiselect('Country', df['country'].dropna().unique()),
        'origin': st.sidebar.multiselect('Origin', df['origin'].dropna().unique()),
        'destination': st.sidebar.multiselect('Destination', df['destination'].dropna().unique()),
        'transit': st.sidebar.multiselect('Transit', df['transit'].dropna().unique()),
        'aircraft_1': st.sidebar.multiselect('Aircraft 1', df['aircraft_1'].dropna().unique()),
        'aircraft_2': st.sidebar.multiselect('Aircraft 2', df['aircraft_2'].dropna().unique()),
        'type': st.sidebar.multiselect('Type', df['type'].dropna().unique()),
        'seat_type': st.sidebar.multiselect('Seat Type', df['seat_type'].dropna().unique()),
        'experience': st.sidebar.multiselect('Experience', df['experience'].dropna().unique()),
        'month_review_num': st.sidebar.multiselect('Month of Review', range(1, 13), default=list(range(1, 13))),
        'year_review': st.sidebar.multiselect('Year of Review', range(df['date_review'].dt.year.min(), df['date_review'].dt.year.max() + 1))
    }

    df_filtered = filter_data(df, filters)

    st.title('Flight Reviews')

    # Metrics
    all_time_metrics = calculate_metrics(df_filtered)
    display_metrics(all_time_metrics, 'All Time')

    current_date = datetime.now()
    this_month_df = df_filtered[
        (df_filtered['date_review'].dt.month == current_date.month) & 
        (df_filtered['date_review'].dt.year == current_date.year)
    ]
    this_month_metrics = calculate_metrics(this_month_df)
    display_metrics(this_month_metrics, f'This Month ({current_date.strftime("%B - %Y")})')

    # Charts
    st.header('Chart breakdown')

    breakdown_column = st.selectbox("Select the category for breakdown:", options=['type', 'seat_type'])

    col1, col2 = st.columns(2)
    with col1:
        fig = create_chart(df_filtered.groupby([breakdown_column, 'experience']).size().reset_index(name='count'),
                           x=breakdown_column, y='count', color='experience', 
                           title=f'Experience Breakdown by {breakdown_column.capitalize()}',
                           color_map=COLOR_MAP_EXPERIENCE)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = create_chart(df_filtered['experience'].value_counts(normalize=True) * 100,
                           title='Experience Overview', color_map=COLOR_MAP_EXPERIENCE, chart_type='pie')
        st.plotly_chart(fig, use_container_width=True)

    # Add more charts as needed...

if __name__ == "__main__":
    main()