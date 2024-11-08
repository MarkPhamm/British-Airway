import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

# Function to create a bar chart or donut chart of experience 
def plot_experience(df, breakdown_column, chart_type='distribution'):
    df['experience'] = pd.Categorical(df['experience'], categories=['Poor', 'Fair', 'Good'], ordered=True)
    
    if chart_type == 'distribution':
        experience_by_breakdown = df.groupby([breakdown_column, 'experience'], observed=False).size().reset_index(name='count')

        color_map = {
            'Poor': '#e63946',  
            'Fair': '#f4a261', 
            'Good': '#2a9d8f'   
        }

        fig = px.bar(experience_by_breakdown, x=breakdown_column, y='count', color='experience',
                     color_discrete_map=color_map,
                     title=f'Experience Breakdown by {breakdown_column.capitalize()}')
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, legend_title_text='Experience')
    
    elif chart_type == 'composition':
        experience_counts = df.groupby(breakdown_column)['experience'].value_counts(normalize=True).unstack().fillna(0) * 100
        
        color_map = {
            'Poor': '#e63946',  
            'Fair': '#f4a261', 
            'Good': '#2a9d8f'   
        }
        colors = [color_map[x] for x in experience_counts.columns]
        
        fig = go.Figure(data=[go.Pie(labels=experience_counts.columns, 
                                     values=experience_counts.sum(), 
                                     hole=.5,  
                                     marker_colors=colors, 
                                     pull=[0.02] * len(experience_counts.columns)  
                                    )])
        fig.update_layout(title_text='Experience Overview by ' + breakdown_column.capitalize(),  
                          showlegend=True 
                         )
    
    return fig

# Function to create a bar chart or donut chart of recommendations 
def plot_recommendation(df, breakdown_column, chart_type='distribution'):
    df['recommended'] = pd.Categorical(df['recommended'], categories=[False, True], ordered=True)
    
    if chart_type == 'distribution':
        recommendation_by_breakdown = df.groupby([breakdown_column, 'recommended'], observed=False).size().reset_index(name='count')

        color_map = {
            False: '#e63946',  
            True: '#2a9d8f'   
        }

        fig = px.bar(recommendation_by_breakdown, x=breakdown_column, y='count', color='recommended',
                     color_discrete_map=color_map,
                     title=f'Recommendation Breakdown by {breakdown_column.capitalize()}')
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, legend_title_text='Recommendation')
    
    elif chart_type == 'composition':
        recommendation_counts = df.groupby(breakdown_column)['recommended'].value_counts(normalize=True).unstack().fillna(0) * 100
        
        color_map = {
            False: '#e63946',  
            True: '#2a9d8f'   
        }
        colors = [color_map[x] for x in recommendation_counts.columns]
        
        fig = go.Figure(data=[go.Pie(labels=recommendation_counts.columns, 
                                     values=recommendation_counts.sum(), 
                                     hole=.5,  
                                     marker_colors=colors, 
                                     pull=[0.02] * len(recommendation_counts.columns)  
                                    )])
        fig.update_layout(title_text='Recommendation Overview by ' + breakdown_column.capitalize(),  
                          showlegend=True 
                         )
    
    return fig

# Function to create histogram of score
def plot_score_histogram(df):
    data = df['score'].dropna()

    bar_color = '#2a9d8f' 
    border_color = 'white'  

    fig = go.Figure(data=[go.Histogram(
        x=data, 
        nbinsx=5,  # Lowered the number of bins
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
    return fig

# Function to create box plots of ratings
def plot_rating_boxplots(df, breakdown_column):
    fig = go.Figure()

    for col in breakdown_column:
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

# Function to plot the average money value, score, and recommendation percentage by year
def plot_dual_axis_metrics(df):
    df['year'] = pd.to_datetime(df['date_review']).dt.year
    
    avg_money_value_by_year = df.groupby('year')['money_value'].mean()
    avg_score_by_year = df.groupby('year')['score'].mean()
    
    # Ensure 'recommended' is numeric before calculating the mean
    df['recommended'] = pd.to_numeric(df['recommended'], errors='coerce')
    
    # Convert 'recommended' to a boolean type if it is categorical
    if df['recommended'].dtype.name == 'category':
        df['recommended'] = df['recommended'].cat.codes
    
    avg_recommendation_percentage_by_year = df.groupby('year')['recommended'].mean() * 100
    
    fig = go.Figure()

    # Adding traces for average money value, score, and recommendation percentage
    fig.add_trace(go.Scatter(x=avg_money_value_by_year.index, y=avg_money_value_by_year, mode='lines+markers', name='Avg Money Value'))
    fig.add_trace(go.Scatter(x=avg_score_by_year.index, y=avg_score_by_year, mode='lines+markers', name='Avg Score', yaxis='y'))
    fig.add_trace(go.Scatter(x=avg_recommendation_percentage_by_year.index, y=avg_recommendation_percentage_by_year, mode='lines+markers', name='Avg Recommendation %', yaxis='y2'))

    # Update layout with two y-axes
    fig.update_layout(
        title='Average Money Value, Score & Recommendation Percentage by Year',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Score / Money Value', side='left', position=0, tickvals=[1, 2, 3, 4, 5], ticktext=[1, 2, 3, 4, 5]),
        yaxis2=dict(title='Percentage', side='right', overlaying='y', position=1, tickvals=[0, 10, 20, 30, 40, 50], ticktext=[0, 10, 20, 30, 40, 50]),
        legend=dict(title='Metrics', x=1, y=1, xanchor='right', yanchor='top')  # Positioning legend at top right
    )
    fig.update_layout(width=1000)  # Ensuring the chart is full length
    return fig

# Function to create stacked bar plots of service ratings by year
def plot_service_ratings(df, service_column):
    df[service_column] = pd.Categorical(df[service_column], categories=[1, 2, 3, 4, 5], ordered=True)
    service_rating_counts = df.groupby(['year_review', service_column], observed=False).size().reset_index(name='count')

    fig = px.bar(service_rating_counts, x='year_review', y='count', color=service_column,
                 title=f'Yearly Distribution of {service_column.capitalize()} Ratings',
                 labels={'count':'Count of Ratings', service_column:'Rating'},
                 color_discrete_map={1: '#e63946', 2: '#f4a261', 3: '#f1faee', 4: '#a8dadc', 5: '#2a9d8f'})
    fig.update_layout(barmode='stack', xaxis_title='Year', yaxis_title='Count of Ratings', xaxis={'type': 'category'}, 
                      legend_title_text='Rating', 
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

def plot_country_distribution(df, service_column):
    # Ensure the service column is numeric before calculating the average
    df[service_column] = pd.to_numeric(df[service_column], errors='coerce')

    # Group by country and calculate the average of the service column
    country_avg_rating = df.groupby('country')[service_column].mean().reset_index(name='average_rating')

    # Create a map chart using Plotly Express with green and red color scale
    fig = px.choropleth(country_avg_rating,
                        locations='country',
                        locationmode='country names',
                        color='average_rating',
                        hover_name='country',
                        title=f'Average {service_column.capitalize()} Ratings by Country',
                        color_continuous_scale=['#e63946', '#2a9d8f'])  # Changed color scale to specific colors

    fig.update_layout(geo=dict(showcoastlines=True, coastlinecolor="grey"),  # Changed coastline color to grey
                      xaxis_title='Country',
                      yaxis_title='Average Rating',
                      legend_title_text='Average Rating',
                      legend=dict(x=0, y=1, traceorder='normal', orientation='h', font=dict(size=10), bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)', borderwidth=0),  # Smaller legend font size
                      width=1000,  # Full tab width
                      height=600,  # Increase the height of the plot
                      paper_bgcolor='rgba(0,0,0,0)',  # Make background transparent
                      plot_bgcolor='rgba(0,0,0,0)',  # Make plot area background transparent
                      geo_bgcolor='rgba(0,0,0,0)')  # Make geo background transparent

    return fig

@st.cache_resource
def get_pyg_app(df: pd.DataFrame) -> StreamlitRenderer:
    """Get the Pygwalker app instance."""
    return StreamlitRenderer(df)
