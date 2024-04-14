import streamlit as st
import pandas as pd
import os 
import warnings
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import boto3
from io import StringIO
warnings.filterwarnings("ignore")

# Function to create a bar chart of experience 
def create_experience_chart(df, breakdown_column):
    df['experience'] = pd.Categorical(df['experience'], categories=['Poor', 'Fair', 'Good'], ordered=True)
    experience_by_breakdown = df.groupby([breakdown_column, 'experience']).size().reset_index(name='count')

    color_map = {
        'Poor': '#e63946',  
        'Fair': '#f4a261', 
        'Good': '#2a9d8f'   
    }

    fig = px.bar(experience_by_breakdown, x=breakdown_column, y='count', color='experience',
                 color_discrete_map=color_map,
                 title=f'Experience Breakdown by {breakdown_column.capitalize()}')
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, legend_title_text='Experience')
    return fig

# Function to create a donut chart of experience 
def create_experience_overview(df):
    experience_counts = df['experience'].value_counts(normalize=True) * 100
    
    color_map = {
        'Poor': '#e63946',  
        'Fair': '#f4a261', 
        'Good': '#2a9d8f'   
    }
    colors = [color_map[x] for x in experience_counts.index]
    
    fig = go.Figure(data=[go.Pie(labels=experience_counts.index, 
                                 values=experience_counts.values, 
                                 hole=.5,  
                                 marker_colors=colors, 
                                 pull=[0.02, 0.02, 0.02]  
                                )])
    fig.update_layout(title_text='Experience Overview',  
                      showlegend=True 
                     )
    return fig

# Function to create a bar chart of recommendation %
def create_recommendation_chart(df, breakdown_column):
    df['recommended'] = pd.Categorical(df['recommended'], categories=[False, True], ordered=True)
    experience_by_type = df.groupby([breakdown_column, 'recommended']).size().reset_index(name='count')

    color_map = {
        True: '#2a9d8f', 
        False: '#e63946',  
    }

    fig = px.bar(experience_by_type, x=breakdown_column, y='count', color='recommended',
                 color_discrete_map=color_map,
                 title='Recommendation Breakdown')
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, legend_title_text='Recommendation')
    return fig

# Function to create a donut chart of recommendation
def create_recommendation_overview(df):
    recommendation_counts = df['recommended'].value_counts(normalize=True) * 100

    color_map = {
        False: '#e63946',  
        True: '#2a9d8f'   
    }
    colors = [color_map[x] for x in recommendation_counts.index]
    
    fig = go.Figure(data=[go.Pie(labels=recommendation_counts.index, 
                                 values=recommendation_counts.values, 
                                 hole=.5,  
                                 marker_colors=colors, 
                                 pull=[0.02, 0.02, 0.02]  
                                )])
    fig.update_layout(title_text='Recommendation Overview',  
                      showlegend=True 
                     )
    return fig

# Function to create histogram of score
def create_score_histogram(df):
    data = df['score'].dropna()

    bar_color = '#2a9d8f' 
    border_color = 'white'  

    kde = np.histogram(data, bins=10, density=True)
    kde_xs = (kde[1][:-1] + kde[1][1:]) / 2 
    kde_ys = kde[0]

    fig = go.Figure(data=[go.Histogram(
        x=data, 
        nbinsx=20, 
        name='Histogram', 
        histnorm='probability density',
        marker=dict(
            color=bar_color,  
            line=dict(color=border_color, width=1.5) 
        )
    )])
    fig.update_layout(
        title='Histogram for Score',
        xaxis_title='Score',
        yaxis_title='Density',
        legend_title_text='Distribution',
        template='plotly_white' 
    )
    fig.add_trace(go.Scatter(x=kde_xs, y=kde_ys, mode='lines', name='KDE'))
    return fig

# Function to create box plots of ratings
def create_plot_rating_distributions(df, columns):
    fig = go.Figure()

    for col in columns:
        fig.add_trace(go.Box(y=df[col], name=col))
    
    fig.update_layout(
        title_text='Distribution of Ratings for Various Services',
        yaxis=dict(
            title='Ratings',
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['1', '2', '3', '4', '5']
        ),
        xaxis=dict(title='Service Categories'),
        boxmode='group'
    )
    return fig

# Function to create stacked bar plots of service ratings by year
def create_service_rating_distribution_chart(df, service_column):
    df[service_column] = pd.Categorical(df[service_column], categories=[1, 2, 3, 4, 5], ordered=True)
    service_rating_counts = df.groupby(['year_review', service_column]).size().reset_index(name='count')

    fig = px.bar(service_rating_counts, x='year_review', y='count', color=service_column,
                 title=f'Yearly Distribution of {service_column.capitalize()} Ratings',
                 labels={'count':'Count of Ratings', service_column:'Rating'},
                 color_discrete_map={1: '#e63946', 2: '#f4a261', 3: '#f1faee', 4: '#a8dadc', 5: '#2a9d8f'})
    fig.update_layout(barmode='stack', xaxis_title='Year', yaxis_title='Count of Ratings', xaxis={'type': 'category'}, 
                      legend_title_text='Rating', 
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

# Function to create a map chart for the country column
def create_country_map_chart(df):
    country_counts = df['country'].value_counts()
    fig = px.choropleth(df, locations=country_counts.index, locationmode='country names', color=country_counts.values, title='Country Distribution')
    return fig

# Function to create a pie chart for type
def create_type_pie_chart(df):
    type_counts = df['type'].value_counts(normalize=True) * 100
    fig = go.Figure(data=[go.Pie(labels=type_counts.index, values=type_counts.values)])
    fig.update_layout(title='Type Distribution (%)')
    return fig

# Function to create a pie chart for seat type
def create_seat_type_pie_chart(df):
    seat_type_counts = df['seat_type'].value_counts(normalize=True) * 100
    fig = go.Figure(data=[go.Pie(labels=seat_type_counts.index, values=seat_type_counts.values)])
    fig.update_layout(title='Seat Type Distribution (%)')
    return fig

# Function to create a map chart for the country column
def create_country_map_chart(df):
    country_counts = df['country'].value_counts()
    fig = px.choropleth(df, locations=country_counts.index, locationmode='country names', color=country_counts.values, title='Country Distribution', color_continuous_scale='Blues')
    return fig

# Function to create a bar chart for the country column
def create_country_bar_chart(df):
    country_counts = df['country'].value_counts()
    fig = px.bar(x=country_counts.index, y=country_counts.values, title='Country Distribution')
    fig.update_xaxes(title='Country')
    fig.update_yaxes(title='Count')
    return fig

def create_top_origin_bar_chart(df):
    top_origin = df['origin'].value_counts().head(5)
    fig = px.bar(x=top_origin.index, y=top_origin.values, title='Top 5 Most Common Origin Airports')
    fig.update_xaxes(title='Airport')
    fig.update_yaxes(title='Count')
    return fig

def create_top_destination_bar_chart(df):
    top_destination = df['destination'].value_counts().head(5)
    fig = px.bar(x=top_destination.index, y=top_destination.values, title='Top 5 Most Common Destination Airports')
    fig.update_xaxes(title='Airport')
    fig.update_yaxes(title='Count')
    return fig

def create_top_aircraft_bar_chart(df):
    top_aircraft = df['aircraft'].value_counts().head(5)
    fig = px.bar(x=top_aircraft.index, y=top_aircraft.values, title='Top 5 Most Common Aircraft')
    fig.update_xaxes(title='Aircraft')
    fig.update_yaxes(title='Count')
    return fig

def create_top_seat_comfort_bar_chart(df):
    # Filter the DataFrame to include only aircraft with count > 20
    filtered_df = df[df.groupby('aircraft')['aircraft'].transform('size') > 20]
    
    # Calculate the average seat comfort ratings
    avg_seat_comfort = filtered_df.groupby('aircraft')['seat_comfort'].mean().nlargest(5)
    
    # Create the bar chart
    fig = px.bar(x=avg_seat_comfort.index, y=avg_seat_comfort.values, 
                 title='Top 5 Aircraft with Highest Seat Comfort Average')
    fig.update_xaxes(title='Aircraft')
    fig.update_yaxes(title='Average Seat Comfort Rating')
    return fig

def create_average_score_by_year(df):
    df['year'] = pd.to_datetime(df['date_review']).dt.year
    avg_score_by_year = df.groupby('year')['score'].mean().reset_index()

    fig = px.line(avg_score_by_year, x='year', y='score', title='Average Score by Year')
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Average Score')
    return fig

# Function to plot the average money value and score by year
def create_combined_average_plot(df):
    df['year'] = pd.to_datetime(df['date_review']).dt.year
    
    avg_money_value_by_year = df.groupby('year')['money_value'].mean()
    avg_score_by_year = df.groupby('year')['score'].mean() 

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=avg_money_value_by_year.index, y=avg_money_value_by_year, mode='lines+markers', name='Avg Money Value'))
    fig.add_trace(go.Scatter(x=avg_score_by_year.index, y=avg_score_by_year, mode='lines+markers', name='Avg Score'))
    fig.update_layout(
        title='Average Money Value & Score by Year',
        xaxis_title='Year',
        yaxis_title='Average Value / Score',
        legend_title_text='Metrics'
    )
    return fig

# Function to plot the average % of recommendation by year
def create_average_recommendation_percentage_by_year(df):
    df['year'] = pd.to_datetime(df['date_review']).dt.year
    df['recommended'] = df['recommended'].astype(int)

    avg_recommendation_percentage_by_year = df.groupby('year')['recommended'].mean() * 100
    avg_recommendation_percentage_by_year = avg_recommendation_percentage_by_year.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=avg_recommendation_percentage_by_year['year'], y=avg_recommendation_percentage_by_year['recommended'], mode='lines+markers', name='Avg Recommendation %'))
    fig.update_layout(
        title='Average Recommendation Percentage by Year',
        xaxis_title='Year',
        yaxis_title='Average Recommendation %',
        legend_title_text='Metric'
    )
    return fig

def create_review_count_by_year(df):
    df['year'] = pd.to_datetime(df['date_review']).dt.year

    review_count_by_year = df.groupby('year').size().reset_index(name='review_count')

    fig = px.line(review_count_by_year, x='year', y='review_count', title='Review Count by Year')
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Review Count')
    return fig

def create_combined_plot(df):
    df['year'] = pd.to_datetime(df['date_review']).dt.year
    
    avg_money_value_by_year = df.groupby('year')['money_value'].mean()
    avg_score_by_year = df.groupby('year')['score'].mean()
    avg_recommendation_percentage_by_year = df.groupby('year')['recommended'].mean() * 100
    
    fig = go.Figure()

    # Adding traces for average money value and score
    fig.add_trace(go.Scatter(x=avg_money_value_by_year.index, y=avg_money_value_by_year, mode='lines+markers', name='Avg Money Value'))
    fig.add_trace(go.Scatter(x=avg_score_by_year.index, y=avg_score_by_year, mode='lines+markers', name='Avg Score', yaxis='y'))

    # Adding trace for average recommendation percentage
    fig.add_trace(go.Scatter(x=avg_recommendation_percentage_by_year.index, y=avg_recommendation_percentage_by_year, mode='lines+markers', name='Avg Recommendation %', yaxis='y2'))

    # Update layout with two y-axes
    fig.update_layout(
        title='Average Metrics by Year',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Score', side='left', position= 0, tickvals=[1, 2, 3, 4, 5], ticktext=[1, 2, 3, 4, 5]),
        yaxis2=dict(title='Percentage', side='right', overlaying='y', position= 1, tickvals=[0, 10, 20, 30, 40, 50], ticktext=[0, 10, 20, 30, 40, 50]),
        legend=dict(title='Metrics')
    )
    return fig

def main():
    # Initialize a session using Amazon S3
    aws_access_key_id = st.secrets['aws_access_key_id']
    aws_secret_access_key = st.secrets['aws_secret_access_key']
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Name of the S3 bucket
    bucket_name = 'british-airway'

    # Function to get the two most recent CSV files
    def get_recent_csv_files(bucket_name, num_files=2):
        csv_files = []
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            if obj['Key'].endswith('.csv'):
                csv_files.append({'Key': obj['Key'], 'LastModified': obj['LastModified']})
        
        # Sort the files by last modified date in descending order and get the top 'num_files' entries
        recent_csv_files = sorted(csv_files, key=lambda x: x['LastModified'], reverse=True)[:num_files]
        return [file['Key'] for file in recent_csv_files]

    # Function to read a CSV file from S3 into a DataFrame
    def read_csv_to_df(bucket_name, file_key):
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))
        return df

    # Get the two most recent CSV files

    recent_csv_files = get_recent_csv_files(bucket_name)

    # You can now loop through the file keys or handle them individually
    # Example: Read the files into DataFrames
    dataframes = [read_csv_to_df(bucket_name, file_key) for file_key in recent_csv_files]

    df= dataframes[0]
    previous_df = dataframes[1]

    # -----------------------------------------------------------

    df['date_review'] = pd.to_datetime(df['date_review']).dt.date

    # Set page configuration
    st.set_page_config(layout="wide")

    # Slicers
    st.sidebar.title('General filters')
    verified_filter = st.sidebar.multiselect('Verified', df['verified'].dropna().unique(), default=None)
    recommended_filter = st.sidebar.multiselect('Recommended', df['recommended'].dropna().unique(), default=None)
    country_filter = st.sidebar.multiselect('Country', df['country'].dropna().unique())
    origin_filter = st.sidebar.multiselect('Origin', df['origin'].dropna().unique())
    destination_filter = st.sidebar.multiselect('Destination', df['destination'].dropna().unique())
    transit_filter = st.sidebar.multiselect('transit', df['transit'].dropna().unique(), default=None)
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

    # Calculate general metrics
    recommendation_percentage = df['recommended'].mean() * 100
    average_money_value = df['money_value'].mean()
    average_service_score = df['score'].mean()
    review_count = len(df)

    # Calculate previous metrics
    previous_recommendation_percentage = previous_df['recommended'].mean() * 100
    previous_average_money_value = previous_df['money_value'].mean()
    previous_average_service_score = previous_df['score'].mean()
    previous_review_count = len(previous_df)
    
    # Calculate changes in metrics
    change_recommendation_percentage = recommendation_percentage - previous_recommendation_percentage
    change_average_money_value = average_money_value - previous_average_money_value
    change_average_service_score = average_service_score - previous_average_service_score
    change_review_count = review_count - previous_review_count


    # Display the percentages as a dashboard
    st.header('General Metrics')
    col1, space1, col2, space2, col3, space3, col4 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1])
    with col1:
        st.metric(label="Recommendation Percentage", value=f"{recommendation_percentage:.2f}%", delta=f"{change_recommendation_percentage:.2f}% from last week")
        st.caption('A higher percentage indicates customers are more likely to recommend.')
    with col2:
        st.metric(label="VFM Score", value=f"{average_money_value:.2f} / 5", delta= f"{change_average_money_value:.3f}% from last week")
        st.caption('A higher score indicates greater satisfaction with the investment.')
    with col3:
        st.metric(label="Service Score", value=f"{average_service_score:.2f} / 5", delta=f"{change_average_service_score:.3f}% from last week")
        st.caption('A higher score indicates greater satisfaction with services.')
    with col4:
        st.metric(label="Total number of review", value=f"{review_count:.0f}", delta=f"+{change_review_count} reviews from last week")
        st.caption('Total number of reviews from Air Quality.')
    st.markdown("&nbsp;")

    # Display the reviews
    if st.checkbox('Show all reviews'):
        st.write(df)
    else:
        st.write("Top 5 most recent reviews")
        st.write(df.head(5))

    # -------------------------------------
    # Chart Breakdown
    st.header('Chart breakdown')

    st.subheader('Experience Breakdown')

    breakdown_column = st.selectbox(
    "Select the category for breakdown:",
    options=['type', 'seat_type']  
    )

    # Experience breakdown
    fig1 = create_experience_chart(df, breakdown_column)
    fig2 = create_experience_overview(df)

    col1, space1, col2 = st.columns([4,0.5, 2])
    with col1:
        st.plotly_chart(fig1, use_container_width=True, height=400, width=50)

    with col2:
        st.plotly_chart(fig2, use_container_width=True, height=300, width=100)

    # Recommendation breakdown
    fig3 = create_recommendation_chart(df, breakdown_column)
    fig4 = create_recommendation_overview(df)

    col1, space1, col2 = st.columns([4,0.5, 2])
    with col1:
        st.plotly_chart(fig3, use_container_width=True, height=400, width=50)
    with col2:
        st.plotly_chart(fig4, use_container_width=True, height=300, width=100)

    # Rating Scores Breakdown
    st.subheader("Rating Scores Breakdown")

    # Score histogram
    fig5 = create_score_histogram(df)
    st.plotly_chart(fig5, use_container_width=True)

    # Ratings boxplots
    rating_columns = ['seat_comfort', 'cabit_serv', 'food', 'ground_service', 'wifi']
    fig6 = create_plot_rating_distributions(df, rating_columns)
    st.plotly_chart(fig6, use_container_width=True, height=600, width=400)
    
    # Time Series
    st.subheader('Time Series')
    df['date_review'] = pd.to_datetime(df['date_review'])

    # Avg score and money_value by year line chart
    fig7 = create_combined_average_plot(df)
    # st.plotly_chart(fig7, use_container_width=True)

    # Avg recommendation rate by year line chart
    fig8 = create_average_recommendation_percentage_by_year(df)
    # st.plotly_chart(fig8, use_container_width=True)

    fig10 = create_combined_plot(df)
    st.plotly_chart(fig10, use_container_width=True)

    # Ratings by year
    service_columns = ['seat_comfort', 'cabit_serv', 'food', 'ground_service', 'wifi'] 
    service_to_plot = st.selectbox('Select a service to plot:', service_columns)
    fig9 = create_service_rating_distribution_chart(df, service_to_plot)
    fig9.update_layout(height=600)
    st.plotly_chart(fig9, use_container_width=True, height=200, width=400)

    # fig10 = create_combined_plot(df)
    # st.plotly_chart(fig10, use_container_width=True)


if __name__ == "__main__":
    main()