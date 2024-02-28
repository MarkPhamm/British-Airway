import pandas as pd
import numpy as np

# Clean country Column: Remove parentheses from the countries column
def clean_country(df):
    df['countries'] = df['countries'].str.replace('(', '').str.replace(')', '')
    return df

# Clean Review Bodies into Bodies and Verified: Split into 
def clean_review(df):
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
    df['Month Year Flown'] = df['Month Year Flown'].dt.strftime('%m/%Y')

    return df
# Clean Review Column: Trim leading spaces in the 'Review' column
def clean_review(df):
    # Remove double quotes in the 'Review' column
    df['Review'] = df['Review'].str.replace('"', '')
    df['Review'] = df['Review'].str.lstrip()
    return df

# Rename columns
def rename_columns(df):
    df = df.rename(columns={
        'verified': 'Verified',
        'review': 'Review',
        'customer_names': 'Customer Name',
        'countries': 'Country'
    })
    return df

# Reorder Columns
def reorder_columns(df):
    df =df[['Dates Review', 'Day Review', 'Month Review','Month Review Number','Year Review','Verified','Review','Customer Name',
        'Month Flown','Month Flown Number', 'Year Flown', 'Month Year Flown','Country', 'Aircraft', 'Type Of Traveller',
        'Seat Type', 'Route','Seat Comfort','Cabin Staff Service', 'Food & Beverages', 'Ground Service',
        'Value For Money', 'Wifi & Connectivity','Recommended' ]]
    return df


def main():
    # change this all to function
    df = pd.read_csv("raw_data.csv")
    df = clean_country(df)
    df = clean_date_review(df)
    df = clean_date_flown(df)
    df = clean_review(df)
    df = rename_columns(df)
    df = reorder_columns(df)
    # Export the DataFrame to a CSV file for business purposes
    df.to_csv('clean_data.csv', index=False)