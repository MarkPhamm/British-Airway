import streamlit as st
import pandas as pd
import os 
import warnings
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
warnings.filterwarnings("ignore")

df = pd.read_csv(os.path.join('dataset/booking_data.csv'), encoding='latin-1')
mapping = {
    "Mon": 1,
    "Tue": 2,
    "Wed": 3,
    "Thu": 4,
    "Fri": 5,
    "Sat": 6,
    "Sun": 7,
}

df["flight_day"] = df["flight_day"].map(mapping)

# Create new columns flight_origin and flight_destination
df['flight_origin'] = df['route'].str[:3]
df['flight_destination'] = df['route'].str[-3:]

def remove_outliers(df, column_name=None):
    """
    Remove outliers from a specific column in the DataFrame based on the interquartile range (IQR) method,
    or remove outliers from all numerical columns if column_name is None.

    Parameters:
    - df: DataFrame
        The DataFrame containing the data.
    - column_name: str or None, default None
        The name of the column for which outliers are to be removed,
        or None to remove outliers from all numerical columns.

    Returns:
    - df_filtered: DataFrame
        The DataFrame with outliers removed.
    """
    if column_name is None:
        numerical_columns = df.select_dtypes(include='number').columns
    else:
        numerical_columns = [column_name]

    total_removed = 0
    total_rows = len(df)

    for col in numerical_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        # Define the lower and upper bounds for outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Remove outliers from the specified column
        removed_rows = len(df) - len(df[(df[col] >= lower_bound) & (df[col] <= upper_bound)])
        total_removed += removed_rows

        # Update DataFrame
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

        # Print the number and percentage of removed values if any rows have been removed
        # if removed_rows > 0:
        #     percentage_removed = (removed_rows / total_rows) * 100
        #     st.write(f"Removed {removed_rows} rows ({percentage_removed:.2f}%) due to outliers in column '{col}'.")

    return df


# Set page configuration
st.set_page_config(layout="wide")

st.header("British Airway Booking Dashboard")

def filter_data(df):
    # Filter the DataFrame
    if (num_passengers_filter or sales_channel_filter or trip_type_filter or purchase_lead_filter_min or purchase_lead_filter_max or length_of_stay_filter_min or length_of_stay_filter_max or flight_hour_filter_min or flight_hour_filter_max or route_filter or booking_origin_filter or wants_extra_baggage_filter or wants_preferred_seat_filter or wants_in_flight_meals_filter or flight_duration_filter_min or flight_duration_filter_max or booking_complete_filter or flight_origin_filter or flight_destination_filter):
        filtered_df = df[
            (df['num_passengers'].isin(num_passengers_filter) if num_passengers_filter else True) &
            (df['sales_channel'].isin(sales_channel_filter) if sales_channel_filter else True) &
            (df['trip_type'].isin(trip_type_filter) if trip_type_filter else True) &
            (df['purchase_lead'].between(purchase_lead_filter_min, purchase_lead_filter_max) if purchase_lead_filter_min or purchase_lead_filter_max else True) &
            (df['length_of_stay'].between(length_of_stay_filter_min, length_of_stay_filter_max) if length_of_stay_filter_min or length_of_stay_filter_max else True) &
            (df['flight_hour'].between(flight_hour_filter_min, flight_hour_filter_max) if flight_hour_filter_min or flight_hour_filter_max else True) &
            (df['flight_day'].isin(flight_day_filter) if flight_day_filter else True) &
            (df['route'].isin(route_filter) if route_filter else True) &
            (df['booking_origin'].isin(booking_origin_filter) if booking_origin_filter else True) &
            (df['wants_extra_baggage'] == wants_extra_baggage_filter if wants_extra_baggage_filter is not None else True) &
            (df['wants_preferred_seat'] == wants_preferred_seat_filter if wants_preferred_seat_filter is not None else True) &
            (df['wants_in_flight_meals'] == wants_in_flight_meals_filter if wants_in_flight_meals_filter is not None else True) &
            (df['flight_duration'].between(flight_duration_filter_min, flight_duration_filter_max) if flight_duration_filter_min or flight_duration_filter_max else True) &
            (df['booking_complete'] == booking_complete_filter if booking_complete_filter is not None else True) &
            (df['flight_origin'].isin(flight_origin_filter) if flight_origin_filter else True) &
            (df['flight_destination'].isin(flight_destination_filter) if flight_destination_filter else True)
        ]
        return filtered_df
    else:
        return df


# Slicers
st.sidebar.title('Filters')

num_passengers_filter = st.sidebar.multiselect('Number of Passengers', df['num_passengers'].unique())
sales_channel_filter = st.sidebar.multiselect('Sales Channel', df['sales_channel'].unique())
trip_type_filter = st.sidebar.multiselect('Trip Type', df['trip_type'].unique())
purchase_lead_filter_min, purchase_lead_filter_max = st.sidebar.slider('Purchase Lead', min(df['purchase_lead']), max(df['purchase_lead']), (min(df['purchase_lead']), max(df['purchase_lead'])))
length_of_stay_filter_min, length_of_stay_filter_max = st.sidebar.slider('Length of Stay', min(df['length_of_stay']), max(df['length_of_stay']), (min(df['length_of_stay']), max(df['length_of_stay'])))
flight_hour_filter_min, flight_hour_filter_max = st.sidebar.slider('Flight Hour', min(df['flight_hour']), max(df['flight_hour']), (min(df['flight_hour']), max(df['flight_hour'])))
flight_day_filter = st.sidebar.multiselect('Flight Day', df['flight_day'].unique())
route_filter = st.sidebar.multiselect('Route', df['route'].unique())
booking_origin_filter = st.sidebar.multiselect('Booking Origin', df['booking_origin'].unique())
wants_extra_baggage_filter = st.sidebar.selectbox('Wants Extra Baggage', [None, True, False])
wants_preferred_seat_filter = st.sidebar.selectbox('Wants Preferred Seat', [None, True, False])
wants_in_flight_meals_filter = st.sidebar.selectbox('Wants In-flight Meals', [None, True, False])
flight_duration_filter_min, flight_duration_filter_max = st.sidebar.slider('Flight Duration', min(df['flight_duration']), max(df['flight_duration']), (min(df['flight_duration']), max(df['flight_duration'])))
booking_complete_filter = st.sidebar.selectbox('Booking Complete', [None, True, False])
flight_origin_filter = st.sidebar.multiselect('Flight Origin', df['flight_origin'].unique())
flight_destination_filter = st.sidebar.multiselect('Flight Destination', df['flight_destination'].unique())

# Apply filters
df = filter_data(df)

st.header('General Metrics')

# Define lists of categorical and numerical columns
categorical_columns_pie = ['num_passengers', 'sales_channel', 'trip_type', 'flight_day', 'wants_extra_baggage', 'wants_preferred_seat', 'wants_in_flight_meals', 'booking_complete']
categorical_columns_bar = ['booking_origin', 'flight_origin', 'flight_destination', 'route']
categorical_columns = categorical_columns_pie + categorical_columns_bar
numerical_columns = [col for col in df.columns if col not in categorical_columns]

# Dropdown to select a specific column to remove outliers or remove outliers from all numerical columns
remove_outliers_option = st.selectbox("Select a column to remove outliers or remove outliers from all numerical columns:", ['All'] + numerical_columns, index=0)


if remove_outliers_option == 'All':
    df = remove_outliers(df)
elif remove_outliers_option in numerical_columns:
    df = remove_outliers(df, remove_outliers_option)

st.header('')
# Show filtered dataframe
st.write(df.head())

def plot_histogram(df, column):
    fig = go.Figure()

    # Add histogram trace
    fig.add_trace(go.Histogram(x=df[column], histnorm='probability density', name='Histogram'))

    # Add distribution curve
    x_values = np.linspace(df[column].min(), df[column].max(), 100)
    y_values = np.exp(-((x_values - df[column].mean()) ** 2) / (2 * df[column].std() ** 2)) / (df[column].std() * np.sqrt(2 * np.pi))
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='Distribution'))

    # Update layout
    fig.update_layout(title=f'Histogram with Distribution Curve for {column}', xaxis_title=column, yaxis_title='Density')

    return fig

def plot_pie_chart(df, column):
    # Count occurrences of each category in the column
    value_counts = df[column].value_counts().nlargest(10)

    # Create pie chart
    fig = go.Figure(data=[go.Pie(labels=value_counts.index, values=value_counts.values)])

    # Update layout
    fig.update_layout(
        title=f'Pie Chart for top {column}',
        showlegend=True,
        legend=dict(x=0, y=0.1, orientation='v')  # Adjust legend position
    )

    return fig

def plot_bar_chart(df, column):
    # Count occurrences of each category in the column
    value_counts = df[column].value_counts().nlargest(5)

    # Create bar chart
    fig = go.Figure(data=[go.Bar(x=value_counts.index, y=value_counts.values)])

    # Update layout
    fig.update_layout(
        title=f'Bar Chart for top 5 {column}',
        xaxis_title=column,
        yaxis_title='Count'
    )

    return fig

# Display each histogram plot individually with two plots per row
for i in range(0, len(numerical_columns), 2):
    col1, col2 = st.columns(2)
    with col1:
        if i < len(numerical_columns):
            hist_fig1 = plot_histogram(df, numerical_columns[i])
            st.plotly_chart(hist_fig1)
    with col2:
        if i+1 < len(numerical_columns):
            hist_fig2 = plot_histogram(df, numerical_columns[i+1])
            st.plotly_chart(hist_fig2)

# Display each bar chart individually with two charts per row
for i in range(0, len(categorical_columns), 2):
    col1, col2 = st.columns(2)
    with col1:
        if i < len(categorical_columns):
            bar_fig1 = plot_pie_chart(df, categorical_columns[i])
            st.plotly_chart(bar_fig1)
    with col2:
        if i+1 < len(categorical_columns):
            bar_fig2 = plot_pie_chart(df, categorical_columns[i+1])
            st.plotly_chart(bar_fig2)


