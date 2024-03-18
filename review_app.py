import streamlit as st
import pandas as pd
import os 
import warnings
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
warnings.filterwarnings("ignore")

df = pd.read_csv(os.path.join('dataset/clean_data.csv'))

def clean_route(df):
    """
    Clean the 'route' column of the DataFrame and split it into 'origin', 'destination', and 'transit' columns.

    Parameters:
        df (DataFrame): DataFrame containing a 'route' column.

    Returns:
        DataFrame: DataFrame with 'origin', 'destination', and 'transit' columns.
    """
    def split_route(route):
        if pd.isna(route):
            return pd.NA, pd.NA, pd.NA
        if ' to ' in route:
            parts = route.split(' to ')
            origin = parts[0].strip()
            if len(parts) > 1:
                destination, transit = parts[1].split(' via ') if ' via ' in parts[1] else (parts[1], None)
            else:
                destination, transit = None, None
        else:
            parts = route.split('-')
            origin = parts[0].strip()
            destination = parts[1].strip() if len(parts) > 1 else None
            transit = None
        return origin.strip(), destination.strip() if destination else None, transit.strip() if transit else None

    df[['origin', 'destination', 'transit']] = df['route'].apply(split_route).apply(pd.Series)
    # Replace 'LHR' and 'Heathrow' with 'London Heathrow' in all columns
    df[['origin', 'destination', 'transit']] = df[['origin', 'destination', 'transit']].replace({
        'LHR': 'London Heathrow',
        'Heathrow': 'London Heathrow',
        'London Heatrow': 'London Heathrow',
        'London-Heathrow': 'London Heathrow',
        'London heathrow': 'London Heathrow',
        'London Heaathrow': 'London Heathrow',
        'London UK (Heathrow)': 'London Heathrow',
        'Heathrow (London)': 'London Heathrow',
        'Gatwick':'London Gatwick',
        'LGW':'London Gatwick',
    })

    return df

def split_aircraft_column(df):
    # Split the 'aircraft' column by '/', then by '-', ',', and '&'
    split_aircraft = df['aircraft'].str.split('/|-|,|&', expand=True)
    
    # Rename the columns
    split_aircraft.columns = [f'aircraft_{i+1}' for i in range(split_aircraft.shape[1])]
    
    split_aircraft = split_aircraft[['aircraft_1','aircraft_2']]
    # Concatenate the split columns with the original DataFrame
    df = pd.concat([df, split_aircraft], axis=1)
    
    return df

def clean_aircraft(df, column_name):
    df[column_name] = df[column_name].str.replace(r'(?i)Boeing (\d+)', r'B\1', regex=True)
    df[column_name] = df[column_name].str.replace(r'(?i)777', 'B777')
    df[column_name] = df[column_name].str.replace(r'(?i)A(\d+)', r'A\1', regex=True)
    df[column_name] = df[column_name].str.replace(r'(?i)170', 'E170')
    df[column_name] = df[column_name].str.replace(r'(?i)190', 'E190')
    
    # # Extract 'A___' if present, else keep the same
    # df[column_name] = np.where(df[column_name].str.contains(r'(?i)A\d+'), df[column_name].str.extract(r'(?i)(A\d+)'), df[column_name])
    df[column_name] = df[column_name].str.extract(r'(?i)([A-Z]\d+)', expand=False)
    
    return df

def replace_yes_no_with_bool(df, column):
    """
    Replace 'Yes' and 'No' in the specified column of the DataFrame with True and False respectively.
    
    Parameters:
        df (DataFrame): The DataFrame containing the column to be modified.
        column (str): The name of the column to be modified.
        
    Returns:
        DataFrame: The modified DataFrame with 'Yes' and 'No' replaced with True and False respectively.
    """
    df[column] = df[column].replace({'yes': True, 'no': False})
    return df


def calculate_experience(df):
    conditions = [
        (df['money_value'] <= 2),
        (df['money_value'] == 3),
        (df['money_value'] >= 4)
    ]

    choices = ['poor', 'fair', 'good']

    df['experience'] = np.select(conditions, choices, default='unknown')
    return df

def calculate_service_score(df):
    # Calculate the average score (Assume the weight is equal)
    df['score'] = df[['seat_comfort', 'cabit_serv', 'food', 'ground_service', 'wifi']].mean(axis=1)
    return df



df = clean_route(df)
df = split_aircraft_column(df)
df = clean_aircraft(df, "aircraft_1")
df = clean_aircraft(df, "aircraft_2")
df = replace_yes_no_with_bool(df, "recommended")
df = calculate_experience(df)
df = calculate_service_score(df)
df['date_review'] = pd.to_datetime(df['date_review'])
df = df[['id','verified', 'date_review', 'day_review', 'month_review', 'month_review_num',
       'year_review', 'name', 'month_fly', 'month_fly_num',
       'year_fly', 'month_year_fly', 'country', 'aircraft', 'type',
       'seat_type', 'route','origin', 'destination', 'transit', 'aircraft_1', 'aircraft_2',
         'seat_comfort', 'cabit_serv', 'food','ground_service', 'wifi', 'money_value','score','experience', 'recommended', 'review',
       ]]

print(df.columns)


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


df = filter_data(df)

# Streamlit app
st.title('Flight Reviews')

# Calculate percentage of recommendation
recommendation_percentage = df['recommended'].mean() * 100

# Calculate percentage of verification
verification_percentage = df['verified'].mean() * 100

average_money_value = df['money_value'].mean()

average_service_score = df['score'].mean()

review_count = len(df)

# Display the percentages as a dashboard
st.header('General Metrics')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="Percentage of Recommendation", value=f"{recommendation_percentage:.2f}%", delta=None)
col2.metric(label="Percentage of Verification", value=f"{verification_percentage:.2f}%", delta=None)
col3.metric(label="Average Money Value Score", value=f"{average_money_value:.2f}", delta=None)
col4.metric(label="Average Service Score", value=f"{average_service_score:.2f}", delta=None)
col5.metric(label="Total number of review", value=f"{review_count:.0f}", delta=None)


st.markdown("&nbsp;")

st.write("Top 5 most recent review")
st.table(df.iloc[0:5])

st.header('Chart breakdown')
# Function to create a pie chart of experience count %
def create_experience_pie_chart(df):
    experience_counts = df['experience'].value_counts(normalize=True) * 100
    fig = go.Figure(data=[go.Pie(labels=experience_counts.index, values=experience_counts.values)])
    fig.update_layout(title='Experience Breakdown (%)')
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
    fig = px.choropleth(df, locations=country_counts.index, locationmode='country names', color=country_counts.values, title='Country Distribution')
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
    # Convert date_review to datetime
    df['date_review'] = pd.to_datetime(df['date_review'])
    
    # Extract year from date_review
    df['year'] = df['date_review'].dt.year
    
    # Calculate average score by year
    avg_score_by_year = df.groupby('year')['score'].mean().reset_index()

    # Plot
    fig = px.line(avg_score_by_year, x='year', y='score', title='Average Score by Year')
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Average Score')
    return fig

# Function to plot the average money value by year
def create_average_money_value_by_year(df):
    # Convert date_review to datetime
    df['date_review'] = pd.to_datetime(df['date_review'])
    
    # Extract year from date_review
    df['year'] = df['date_review'].dt.year
    
    # Calculate average money value by year
    avg_money_value_by_year = df.groupby('year')['money_value'].mean().reset_index()

    # Plot
    fig = px.line(avg_money_value_by_year, x='year', y='money_value', title='Average Money Value by Year')
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Average Money Value')
    return fig



# Split the layout into two columns
col1, col2 = st.columns(2)

# Graph 1: Pie chart of experience count %
fig1 = create_experience_pie_chart(df)
col1.plotly_chart(fig1, use_container_width=True, height=400, width=400)

# Graph 2: Pie chart for type
fig2 = create_type_pie_chart(df)
col2.plotly_chart(fig2, use_container_width=True, height=400, width=400)

# Graph 3: Pie chart for seat type
fig3 = create_country_map_chart(df)
col1.plotly_chart(fig3, use_container_width=True, height=400, width=400)

fig4 = create_country_bar_chart(df)
col2.plotly_chart(fig4, use_container_width=True, height=400, width=400)

fig5 = create_top_origin_bar_chart(df)
col1.plotly_chart(fig5, use_container_width=True, height=400, width=400)

fig6 = create_top_destination_bar_chart(df)
col2.plotly_chart(fig6, use_container_width=True, height=400, width=400)

fig7 = create_top_aircraft_bar_chart(df)
col1.plotly_chart(fig7, use_container_width=True, height=400, width=400)

fig8 = create_top_seat_comfort_bar_chart(df)
col2.plotly_chart(fig8, use_container_width=True, height=400, width=400)

fig9 = create_average_score_by_year(df)
col1.plotly_chart(fig9, use_container_width=True, height=400, width=400)

fig10 = create_average_money_value_by_year(df)
col2.plotly_chart(fig10, use_container_width=True, height=400, width=400)






