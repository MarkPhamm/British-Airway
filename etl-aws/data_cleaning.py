import pandas as pd
import numpy as np
import os

def clean_country(df):
    # Remove parentheses from the countries column
    df['countries'] = df['countries'].str.replace('(', '').str.replace(')', '')
    return df

def clean_review(df):
    # Clean Review Bodies into Bodies and Verified
    if df['review_bodies'] is None:
        df.drop(columns=['review_bodies'], inplace=True)
    # Split the review_bodies column into two separate columns
    split_df = df['review_bodies'].str.split('|', expand=True)

    # If the split results in only one column, assign the first column to 'review' and set 'verified' to None
    if len(split_df.columns) == 1:
        split_df.columns = ['review']
        split_df['verified'] = None
    else:
        split_df.columns = ['verified', 'review']

    # Assign the split columns to the DataFrame
    df[['verified', 'review']] = split_df

    # Check if the review column is None and the verified column is not None
    mask = (df['review'].isnull()) & (df['verified'].notnull())

    # Swap values between review and verified columns where the condition is met
    df.loc[mask, ['review', 'verified']] = df.loc[mask, ['verified', 'review']].values

    # Assuming df is your DataFrame
    df.drop(columns=['review_bodies'], inplace=True)

    # Check if 'verified' column contains 'Trip Verified' and replace with True, else replace with False
    df['verified'] = df['verified'].str.contains('Trip Verified', case=False, na=False)

    return df

# Cleaned dates column and split it into Date Review, Day Review, Month Review, Year Review 
def clean_date_review(df):
    # Split the 'dates' column into separate columns for day, month, and year
    df[['Day Review', 'Month Review', 'Year Review']] = df['dates'].str.split(expand=True)

    # Remove the last 2 characters from the 'Day Review' column
    df['Day Review'] = df['Day Review'].str[:-2]

    # Concatenate 'Day Review', 'Month Review', and 'Year Review' into a single string
    date_strings = df['Day Review'] + ' ' + df['Month Review'] + ' ' + df['Year Review']

    # Create the 'Dates' column by converting the concatenated strings to datetime objects
    df['Dates Review'] = pd.to_datetime(date_strings, format='%d %B %Y')

    # Create the 'Dates Review' column by converting the concatenated strings to datetime objects
    df['Dates Review'] = pd.to_datetime(df['Dates Review'], format='%Y-%m-%d')

    return df

# Clean date flown column to Month Flown and Year Flown
def clean_date_flown(df):
# Rename date flown to month flown
    df.rename(columns={'Date Flown': 'Month Flown'}, inplace=True)

    # Split Month Flown to Month Flown and Year Flown
    df[['Month Flown', 'Year Flown']] = df['Month Flown'].str.split(' ', expand=True)

    # Define a dictionary mapping month names to numerical values
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # Map the month names to their corresponding numerical values and create the "Month Flown Number" column
    df['Month Flown Number'] = df['Month Flown'].map(month_mapping)
    df['Month Review Number'] = df['Month Review'].map(month_mapping)

    # Convert 'Month Flown Number' to string and pad with zero if necessary
    df['Month Flown Number'] = df['Month Flown Number'].replace(['NA', 'inf'], np.nan)  # Replace 'NA' and 'inf' with NaN
    df['Month Flown Number'] = df['Month Flown Number'].astype(float).astype(pd.Int64Dtype())  # Convert to float and then to integer

    # Combine 'Month Flown Number' and 'Year Flown' into a single string
    df['Month Year Flown'] = df['Year Flown'].astype(str) + '-' + df['Month Flown Number'].astype(str).str.zfill(2) + '-' + '01'

    # Convert the combined string to datetime, handling NaN values gracefully
    df['Month Year Flown'] = pd.to_datetime(df['Month Year Flown'], errors='coerce')
    # Format 'Month Year Flown' column to display 'MM/YYYY' format
    df['Month Year Flown'] = df['Month Year Flown'].dt.strftime('%m-%Y')
    return df

# Clean Review Column: Trim leading spaces in the 'Review' column
def clean_space(df):
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def create_id(df):
    df = df.sort_values(by='Dates Review', ascending=False)
    df['id'] = range(len(df))
    return df

# Rename columns
def rename_columns(df):
    # df = df.rename(columns={
    #     'verified': 'Verified',
    #     'review': 'Review',
    #     'customer_names': 'Customer Name',
    #     'countries': 'Country'
    # })
    new_column_names = {
                        'Dates Review': 'date_review',
                        'Day Review': 'day_review',
                        'Month Review': 'month_review',
                        'Month Review Number': 'month_review_num',
                        'Year Review': 'year_review',
                        'customer_names':'name',
                        'Month Flown': 'month_fly',
                        'Month Flown Number': 'month_fly_num',
                        'Year Flown':'year_fly',
                        'Month Year Flown': 'month_year_fly',
                        'countries': 'country',
                        'Aircraft': 'aircraft',
                        'Type Of Traveller': 'type',
                        'Seat Type': 'seat_type',
                        'Route': 'route',
                        'Seat Comfort': 'seat_comfort',
                        'Cabin Staff Service': 'cabit_serv',
                        'Food & Beverages': 'food',
                        'Ground Service': 'ground_service',
                        'Wifi & Connectivity': 'wifi',
                        'Value For Money': 'money_value',
                        'Recommended': 'recommended'
                        }
    df.rename(columns=new_column_names, inplace=True)
    return df

# Reorder Columns
def reorder_columns(df):
    df = df[['id','verified','date_review', 'day_review', 'month_review', 'month_review_num', 'year_review', 'verified','name', 
    'month_fly', 'month_fly_num', 'year_fly', 'month_year_fly', 'country', 'aircraft', 'type', 'seat_type', 'route', 
    'seat_comfort', 'cabit_serv', 'food', 'ground_service', 'wifi', 'money_value', 'recommended','review']]
    return df

# def format_column(df):
#     new_column_names = {'ID':'id',
#                     'Dates Review': 'date_review',
#                     'Day Review': 'day_review',
#                     'Month Review': 'month_review',
#                    'Month Review Number': 'month_review_num',
#                    'Year Review': 'year_review',
#                    'Verified': 'verified',
#                    'Customer Name':'name',
#                    'Month Flown': 'month_fly',
#                    'Month Flown Number': 'month_fly_num',
#                     'Year Flown':'year_fly',
#                    'Month Year Flown': 'month_year_fly',
#                    'Country': 'country',
#                    'Aircraft': 'aircraft',
#                    'Type Of Traveller': 'type',
#                    'Seat Type': 'seat_type',
#                    'Route': 'route',
#                    'Seat Comfort': 'seat_comfort',
#                    'Cabin Staff Service': 'cabit_serv',
#                    'Food & Beverages': 'food',
#                    'Ground Service': 'ground_service',
#                    'Wifi & Connectivity': 'wifi',
#                    'Value For Money': 'money_value',
#                    'Recommended': 'recommended',
#                    'Review': 'review'}
#     df.rename(columns=new_column_names, inplace=True)
#     return df


def main(df):
    df = clean_country(df)
    df = clean_review(df)
    df = clean_date_review(df)
    df = clean_date_flown(df)
    df = clean_space(df)
    df = create_id(df)
    df = rename_columns(df)
    df = reorder_columns(df)
    # df = format_column(df)
    # Drop the first column by its positional index
    # df.drop(df.columns[0], axis=1, inplace=True)
    print(df.dtypes)

    return df
