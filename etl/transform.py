import pandas as pd
import numpy as np
import os
from typing import Dict, List
import logging

def clean_country(df: pd.DataFrame) -> pd.DataFrame:
    df['countries'] = df['countries'].str.replace(r'[()]', '', regex=True)
    return df

def clean_review(df: pd.DataFrame) -> pd.DataFrame:
    if 'review_bodies' not in df.columns:
        return df
    
    split_df = df['review_bodies'].str.split('|', expand=True)
    
    if len(split_df.columns) == 1:
        df['review'] = split_df[0]
        df['verified'] = pd.NA
    else:
        df['verified'], df['review'] = split_df[0], split_df[1]
    
    mask = df['review'].isnull() & df['verified'].notnull()
    df.loc[mask, ['review', 'verified']] = df.loc[mask, ['verified', 'review']].values
    
    df['verified'] = df['verified'].str.contains('Trip Verified', case=False, na=False)
    
    df.drop(columns=['review_bodies'], inplace=True)
    return df

def clean_date_review(df: pd.DataFrame) -> pd.DataFrame:
    df[['Day Review', 'Month Review', 'Year Review']] = df['dates'].str.split(expand=True)
    df['Day Review'] = df['Day Review'].str[:-2]
    
    df['Dates Review'] = pd.to_datetime(
        df['Day Review'] + ' ' + df['Month Review'] + ' ' + df['Year Review'],
        format='%d %B %Y'
    )
    
    return df

def clean_date_flown(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns={'Date Flown': 'Month Flown'}, inplace=True)
    df[['Month Flown', 'Year Flown']] = df['Month Flown'].str.split(' ', expand=True)
    
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    df['Month Flown Number'] = df['Month Flown'].map(month_mapping)
    df['Month Review Number'] = df['Month Review'].map(month_mapping)
    
    df['Month Flown Number'] = pd.to_numeric(df['Month Flown Number'], errors='coerce').astype('Int64')
    
    df['Month Year Flown'] = pd.to_datetime(
        df['Year Flown'].astype(str) + '-' + df['Month Flown Number'].astype(str).str.zfill(2) + '-01',
        format='%Y-%m-%d',
        errors='coerce'
    ).dt.strftime('%m-%Y')
    
    return df

def clean_space(df: pd.DataFrame) -> pd.DataFrame:
    return df.map(lambda x: x.strip() if isinstance(x, str) else x)

def create_id(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(by='Dates Review', ascending=False)
    df['id'] = range(len(df))
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    new_column_names: Dict[str, str] = {
        'Dates Review': 'date_review',
        'Day Review': 'day_review',
        'Month Review': 'month_review',
        'Month Review Number': 'month_review_num',
        'Year Review': 'year_review',
        'customer_names': 'name',
        'Month Flown': 'month_fly',
        'Month Flown Number': 'month_fly_num',
        'Year Flown': 'year_fly',
        'Month Year Flown': 'month_year_fly',
        'countries': 'country',
        'Aircraft': 'aircraft',
        'Type Of Traveller': 'type',
        'Seat Type': 'seat_type',
        'Route': 'route',
        'Seat Comfort': 'seat_comfort',
        'Cabin Staff Service': 'cabin_serv',
        'Food & Beverages': 'food',
        'Ground Service': 'ground_service',
        'Wifi & Connectivity': 'wifi',
        'Value For Money': 'money_value',
        'Recommended': 'recommended'
    }
    return df.rename(columns=new_column_names)

def reorder_columns_before_fe(df: pd.DataFrame) -> pd.DataFrame:
    column_order = [
        'id', 'verified', 'date_review', 'day_review', 'month_review', 'month_review_num', 'year_review',
        'name', 'month_fly', 'month_fly_num', 'year_fly', 'month_year_fly', 'country', 'aircraft', 'type',
        'seat_type', 'route', 'seat_comfort', 'cabin_serv', 'food', 'ground_service', 'wifi', 'money_value',
        'recommended', 'review'
    ]
    return df[column_order]

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = (df.pipe(clean_country)
            .pipe(clean_review)
            .pipe(clean_date_review)
            .pipe(clean_date_flown)
            .pipe(clean_space)
            .pipe(create_id)
            .pipe(rename_columns)
            .pipe(reorder_columns_before_fe))
    return df

def calculate_score(df: pd.DataFrame) -> pd.DataFrame:
    df['score'] = df[['seat_comfort', 'cabin_serv', 'food', 'ground_service', 'wifi']].mean(axis=1)
    return df

def clean_route(df: pd.DataFrame) -> pd.DataFrame:
    def split_route(route: str) -> tuple:
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
    
    airport_replacements = {
        'LHR': 'London Heathrow',
        'Heathrow': 'London Heathrow',
        'London Heatrow': 'London Heathrow',
        'London-Heathrow': 'London Heathrow',
        'London heathrow': 'London Heathrow',
        'London Heaathrow': 'London Heathrow',
        'London UK (Heathrow)': 'London Heathrow',
        'Heathrow (London)': 'London Heathrow',
        'Gatwick': 'London Gatwick',
        'LGW': 'London Gatwick',
    }
    
    df[['origin', 'destination', 'transit']] = df[['origin', 'destination', 'transit']].replace(airport_replacements)

    return df

def split_aircraft_column(df: pd.DataFrame) -> pd.DataFrame:
    split_aircraft = df['aircraft'].str.split('/|-|,|&', expand=True)
    split_aircraft.columns = [f'aircraft_{i+1}' for i in range(split_aircraft.shape[1])]
    split_aircraft = split_aircraft[['aircraft_1', 'aircraft_2']]
    return pd.concat([df, split_aircraft], axis=1)

def clean_aircraft(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    replacements = [
        (r'(?i)Boeing (\d+)', r'B\1'),
        (r'(?i)777', 'B777'),
        (r'(?i)A(\d+)', r'A\1'),
        (r'(?i)170', 'E170'),
        (r'(?i)190', 'E190'),
    ]
    
    for pattern, replacement in replacements:
        df[column_name] = df[column_name].str.replace(pattern, replacement, regex=True)
    
    df[column_name] = df[column_name].str.extract(r'(?i)([A-Z]\d+)', expand=False)
    
    return df

def calculate_experience(df: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        (df['money_value'] <= 2),
        (df['money_value'] == 3),
        (df['money_value'] >= 4)
    ]
    choices = ['Poor', 'Fair', 'Good']
    df['experience'] = np.select(conditions, choices, default='unknown')
    return df

def calculate_service_score(df: pd.DataFrame) -> pd.DataFrame:
    df['score'] = df[['seat_comfort', 'cabin_serv', 'food', 'ground_service', 'wifi']].mean(axis=1)
    return df

def replace_yes_no_with_bool(df: pd.DataFrame, column: str) -> pd.DataFrame:
    with pd.option_context('future.no_silent_downcasting', True):
        df[column] = df[column].replace({'yes': True, 'no': False})
    df[column] = df[column].astype('boolean')
    return df

def reorder_columns_after_fe(df: pd.DataFrame) -> pd.DataFrame:
    column_order = [
        'id', 'date_review', 'day_review', 'month_review', 'month_review_num',
        'year_review', 'verified', 'name', 'month_fly', 'month_fly_num',
        'year_fly', 'month_year_fly', 'country', 'aircraft', 'aircraft_1',
        'aircraft_2', 'type', 'seat_type', 'route', 'origin', 'destination', 'transit', 
        'seat_comfort', 'cabin_serv', 'food', 'ground_service', 'wifi', 'money_value', 
        'score', 'experience', 'recommended', 'review'
    ]
    return df[column_order]

def feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
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

def main() -> pd.DataFrame:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    directory = "data"
    df = pd.read_csv(os.path.join(directory, "raw_data.csv"))
    df = transform(df)
    df.to_csv(os.path.join(directory, "clean_data.csv"), index=False)
    df = feature_engineer(df)
    df.to_csv(os.path.join(directory, "processed_data.csv"), index=False)
    logging.info("Transform succesfully completed")
    return df

if __name__ == "__main__":
    main()
