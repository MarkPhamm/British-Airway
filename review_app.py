import streamlit as st
import pandas as pd
import os 
import warnings
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
    df = df.dropna(subset=['route'])
    # Function to split the route into origin, destination, and transit
    def split_route(route):
        parts = route.split(' to ')
        origin = parts[0]
        if len(parts) > 1:
            destination, transit = parts[1].split(' via ') if ' via ' in parts[1] else (parts[1], None)
        else:
            destination, transit = None, None
        return origin, destination, transit

    # Apply the function to create new columns
    df[['origin', 'destination', 'transit']] = df['route'].apply(split_route).apply(pd.Series)
    # Replace 'LHR' and 'Heathrow' with 'London Heathrow'
    df['origin'] = df['origin'].replace({'LHR': 'London Heathrow', 'Heathrow': 'London Heathrow'})
    df['destination'] = df['destination'].replace({'LHR': 'London Heathrow', 'Heathrow': 'London Heathrow'})
    df['transit'] = df['transit'].replace({'LHR': 'London Heathrow', 'Heathrow': 'London Heathrow'})
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

df = clean_route(df)
df = split_aircraft_column(df)
df = clean_aircraft(df, "aircraft_1")
df = clean_aircraft(df, "aircraft_2")
print(df.columns)


# Streamlit app
st.title('Flight Reviews')

# Slicers
st.sidebar.title('Filters')
verified_filter = st.sidebar.checkbox('Verified')
recommended_filter = st.sidebar.checkbox('Recommended')
country_filter = st.sidebar.multiselect('Country', df['country'].unique())
origin_filter = st.sidebar.multiselect('Origin', df['origin'].unique())
destination_filter = st.sidebar.multiselect('Destination', df['destination'].unique())
transit_filter = st.sidebar.checkbox('Transit')
aircraft_1_filter = st.sidebar.multiselect('Aircraft 1', df['aircraft_1'].unique())
aircraft_2_filter = st.sidebar.multiselect('Aircraft 2', df['aircraft_2'].unique())
type_filter = st.sidebar.multiselect('Type', df['type'].unique())
seat_type_filter = st.sidebar.multiselect('Seat Type', df['seat_type'].unique())

# Filter the DataFrame
filtered_df = df[
    (df['verified'] == verified_filter if verified_filter else True) &
    (df['recommended'] == recommended_filter if recommended_filter else True) &
    (df['country'].isin(country_filter) if country_filter else True) &
    (df['origin'].isin(origin_filter) if origin_filter else True) &
    (df['destination'].isin(destination_filter) if destination_filter else True) &
    (df['transit'] == transit_filter if transit_filter else True) &
    (df['aircraft_1'].isin(aircraft_1_filter) if aircraft_1_filter else True) &
    (df['aircraft_2'].isin(aircraft_2_filter) if aircraft_2_filter else True) &
    (df['type'].isin(type_filter) if type_filter else True) &
    (df['seat_type'].isin(seat_type_filter) if seat_type_filter else True)
]

# Display filtered DataFrame
st.write(filtered_df)






