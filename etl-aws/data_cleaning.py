import pandas as pd
import numpy as np
import os
from typing import Dict

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
        'Cabin Staff Service': 'cabit_serv',
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
        'seat_type', 'route', 'seat_comfort', 'cabit_serv', 'food', 'ground_service', 'wifi', 'money_value',
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

def main() -> pd.DataFrame:
    directory = "data"
    df = pd.read_csv(os.path.join(directory, "raw_data.csv"))
    df = transform(df)
    df.to_csv(os.path.join(directory, "clean_data.csv"), index=False)
    return df

if __name__ == "__main__":
    main()
