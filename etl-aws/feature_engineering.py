import pandas as pd
import numpy as np
import os

def calculate_score(df):
    df['score'] = df[['seat_comfort', 'cabit_serv', 'food', 'ground_service', 'wifi']].mean(axis=1)
    return df

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

def calculate_experience(df):
    conditions = [
        (df['money_value'] <= 2),
        (df['money_value'] == 3),
        (df['money_value'] >= 4)
    ]

    choices = ['Poor', 'Fair', 'Good']

    df['experience'] = np.select(conditions, choices, default='unknown')
    return df

def calculate_service_score(df):
    # Calculate the average score (Assume the weight is equal)
    df['score'] = df[['seat_comfort', 'cabit_serv', 'food', 'ground_service', 'wifi']].mean(axis=1)
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

def reorder_columns_after_fe(df):
    df = df[['id', 'date_review', 'day_review', 'month_review', 'month_review_num',
       'year_review', 'verified', 'name', 'month_fly', 'month_fly_num',
       'year_fly', 'month_year_fly', 'country', 'aircraft','aircraft_1',
       'aircraft_2', 'type', 'seat_type', 'route','origin', 'destination', 'transit', 
       'seat_comfort', 'cabit_serv', 'food','ground_service', 'wifi', 'money_value', 'score', 'experience',
       'recommended', 'review']]
    return df


def feature_engineer(df):
    # change this all to function
    df = calculate_score(df)
    df = clean_route(df)
    df = split_aircraft_column(df)
    df = clean_aircraft(df, 'aircraft_1')
    df = clean_aircraft(df, 'aircraft_2')
    df = calculate_experience(df)
    df = calculate_service_score(df)
    df = replace_yes_no_with_bool(df, 'recommended')
    df = reorder_columns_after_fe(df)
    return df

def main():
    directory = "data"
    # Save DataFrame to CSV
    df = pd.read_csv(os.path.join(directory, "clean_data.csv"))
    df = feature_engineer(df)

    df.to_csv(os.path.join(directory, "processed_data.csv"), index = False)
    return df

if __name__ == "__main__":
    main()
