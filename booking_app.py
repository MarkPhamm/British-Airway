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
    "Mon": 2,
    "Tue": 3,
    "Wed": 4,
    "Thu": 5,
    "Fri": 6,
    "Sat": 7,
    "Sun": 1,
}

df["flight_day_number"] = df["flight_day"].map(mapping)

# Create new columns flight_origin and flight_destination
df['flight_origin'] = df['route'].str[:3]
df['flight_destination'] = df['route'].str[-3:]

def remove_outliers(df, column_names=None):
    """
    Remove outliers from specific columns in the DataFrame based on the interquartile range (IQR) method,
    or remove outliers from all numerical columns if column_names is None.

    Parameters:
    - df: DataFrame
        The DataFrame containing the data.
    - column_names: list or None, default None
        The list of column names for which outliers are to be removed,
        or None to remove outliers from all numerical columns.

    Returns:
    - df_filtered: DataFrame
        The DataFrame with outliers removed.
    """
    if column_names is None:
        numerical_columns = df.select_dtypes(include='number').columns
    else:
        numerical_columns = column_names

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
        percentage_removed = (removed_rows / total_rows) * 100
        st.write(f"Removed {removed_rows} rows ({percentage_removed:.2f}%) due to outliers in column '{col}'.")

    return df


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
        title=f'Pie Chart for {column}',
        showlegend=True,
        legend=dict(x=0, y=0.1, orientation='v')  # Adjust legend position
    )

    return fig

def plot_bar_chart(df, column):
    # Count occurrences of each category in the column
    value_counts = df[column].value_counts().nlargest(10)

    # Create bar chart
    fig = go.Figure(data=[go.Bar(x=value_counts.index, y=value_counts.values)])

    # Update layout
    fig.update_layout(
        title=f'Bar Chart for top {column}',
        xaxis_title=column,
        yaxis_title='Count'
    )

    return fig

# Set page configuration
st.set_page_config(layout="wide")

st.header("British Airway Booking Dashboard")

def filter_data(df):
    # Filter the DataFrame
    filtered_df = df[
        (df['num_passengers'].between(num_passengers_filter[0], num_passengers_filter[1])) &
        (df['sales_channel'].isin(sales_channel_filter) if sales_channel_filter else True) &
        (df['trip_type'].isin(trip_type_filter) if trip_type_filter else True) &
        (df['purchase_lead'].between(purchase_lead_filter_min, purchase_lead_filter_max)) &
        (df['length_of_stay'].between(length_of_stay_filter_min, length_of_stay_filter_max)) &
        (df['flight_hour'].between(flight_hour_filter_min, flight_hour_filter_max)) &
        (df['flight_day'].isin(flight_day_filter) if flight_day_filter else True) &
        (df['route'].isin(route_filter) if route_filter else True) &
        (df['booking_origin'].isin(booking_origin_filter) if booking_origin_filter else True) &
        ((df['wants_extra_baggage'] == wants_extra_baggage_filter) if wants_extra_baggage_filter is not None else True) &
        ((df['wants_preferred_seat'] == wants_preferred_seat_filter) if wants_preferred_seat_filter is not None else True) &
        ((df['wants_in_flight_meals'] == wants_in_flight_meals_filter) if wants_in_flight_meals_filter is not None else True) &
        (df['flight_duration'].between(flight_duration_filter_min, flight_duration_filter_max)) &
        ((df['booking_complete'] == booking_complete_filter) if booking_complete_filter is not None else True) &
        (df['flight_origin'].isin(flight_origin_filter) if flight_origin_filter else True) &
        (df['flight_destination'].isin(flight_destination_filter) if flight_destination_filter else True)
    ]
    return filtered_df

# Slicers
st.sidebar.title('Filters')

booking_complete_filter = st.sidebar.selectbox('Booking Complete', [None, True, False])

st.sidebar.title('Customer detail')
num_passengers_filter = st.sidebar.slider('Number of Passengers', min_value=int(df['num_passengers'].min()), max_value=int(df['num_passengers'].max()), value=(int(df['num_passengers'].min()), int(df['num_passengers'].max())))
sales_channel_filter = st.sidebar.multiselect('Sales Channel', df['sales_channel'].unique())
trip_type_filter = st.sidebar.multiselect('Trip Type', df['trip_type'].unique())
purchase_lead_filter_min, purchase_lead_filter_max = st.sidebar.slider('Purchase Lead', min(df['purchase_lead']), max(df['purchase_lead']), (min(df['purchase_lead']), max(df['purchase_lead'])))
length_of_stay_filter_min, length_of_stay_filter_max = st.sidebar.slider('Length of Stay', min(df['length_of_stay']), max(df['length_of_stay']), (min(df['length_of_stay']), max(df['length_of_stay'])))

st.sidebar.title('customer preference')
wants_extra_baggage_filter = st.sidebar.selectbox('Wants Extra Baggage', [None, True, False])
wants_preferred_seat_filter = st.sidebar.selectbox('Wants Preferred Seat', [None, True, False])
wants_in_flight_meals_filter = st.sidebar.selectbox('Wants In-flight Meals', [None, True, False])

st.sidebar.title('Flight details')
flight_duration_filter_min, flight_duration_filter_max = st.sidebar.slider('Flight Duration', min(df['flight_duration']), max(df['flight_duration']), (min(df['flight_duration']), max(df['flight_duration'])))
flight_hour_filter_min, flight_hour_filter_max = st.sidebar.slider('Flight Hour', min(df['flight_hour']), max(df['flight_hour']), (min(df['flight_hour']), max(df['flight_hour'])))
flight_day_filter = st.sidebar.multiselect('Flight Day', df['flight_day'].unique())

st.sidebar.title('Route and origin')
booking_origin_filter = st.sidebar.multiselect('Booking Origin', df['booking_origin'].unique())
route_filter = st.sidebar.multiselect('Route', df['route'].unique())
flight_origin_filter = st.sidebar.multiselect('Flight Origin', df['flight_origin'].unique())
flight_destination_filter = st.sidebar.multiselect('Flight Destination', df['flight_destination'].unique())

# Apply filters
df = filter_data(df)

# Define lists of categorical and numerical columns
binary_columns = ['wants_extra_baggage','wants_preferred_seat', 'wants_in_flight_meals', 'booking_complete']
nomimal_columns = ['sales_channel', 'trip_type', 'flight_day', 'booking_origin', 'flight_origin', 'flight_destination', 'route']
# 'flight_day_number','flight_hour'
categorical_columns = binary_columns  + nomimal_columns
numerical_columns = [col for col in df.columns if col not in categorical_columns]
print(numerical_columns)

df = df[['num_passengers','flight_duration', 'purchase_lead', 'length_of_stay', 'flight_day_number', 'flight_hour',
         'sales_channel', 'trip_type', 'flight_day', 'booking_origin', 'flight_origin', 'flight_destination', 'route',
         'wants_extra_baggage','wants_preferred_seat', 'wants_in_flight_meals', 'booking_complete']]


remove_outliers_option = st.multiselect("Select column(s) to remove outliers:", ['num_passengers','purchase_lead','length_of_stay', 'flight_duration'])

df = remove_outliers(df, remove_outliers_option)

st.header('')
# Show filtered dataframe
st.header('Sample data')

# Reorder columns:
st.table(df.iloc[0:5])

booking_percentage = df['booking_complete'].mean() * 100
want_extra_bag_percentage = df['wants_extra_baggage'].mean() * 100
want_prefer_seat_percentage = df['wants_preferred_seat'].mean() * 100
wants_in_flight_meals_percentage = df['wants_in_flight_meals'].mean() * 100
total_row = len(df)

# Display the percentages as a dashboard
st.header('General Metrics')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="Booking Completion Percentage", value=f"{booking_percentage:.2f}%", delta=None)
col2.metric(label="Wants Extra Bag Percentage", value=f"{want_extra_bag_percentage:.2f}%", delta=None)
col3.metric(label="Wants Preferred Seat Percentage", value=f"{want_prefer_seat_percentage:.2f}%", delta=None)
col4.metric(label="Wants In-flight Meals Percentage", value=f"{wants_in_flight_meals_percentage:.2f}%", delta=None)
col5.metric(label="Total Rows", value=f"{total_row:.2f}", delta=None)


st.header('Distribution')

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
bar_columns = ['booking_origin','route','flight_origin','flight_destination']
for i in range(0, len(bar_columns), 2):
    col1, col2 = st.columns(2)
    with col1:
        if i < len(bar_columns):
            bar_fig1 = plot_bar_chart(df, bar_columns[i])
            st.plotly_chart(bar_fig1)
    with col2:
        if i+1 < len(bar_columns):
            bar_fig2 = plot_bar_chart(df, bar_columns[i+1])
            st.plotly_chart(bar_fig2)


