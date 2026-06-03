## Load Sites.txt from both Envirostor and Geotracker folders, and combine them into a single list of sites.
import os
import config as cg
import pandas as pd

        
def load_sites(source_folder):
    path = os.path.join(cg.data_folder, source_folder, cg.sites_folder)
    if not os.path.exists(path):
        return pd.DataFrame()

    try:
        df = pd.read_csv(path, sep='\t', header=0, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep='\t', header=0, encoding='cp1252', encoding_errors='ignore')

    return df

def add_addess(df):
    df['ADDRESS'] = df['STREET_NUMBER'].fillna('') + ' ' + df['STREET_NAME'].fillna('')
    return df

def select_columns(df, column_mapping,columns_to_use):
    df = df.rename(columns=column_mapping)
    return df[columns_to_use]

def load_and_select(source_folder, column_mapping, columns_to_use):
    df = load_sites(source_folder)
    if source_folder == cg.Geotracker_folder:
        df = add_addess(df)
    if df.empty:
        print(f"No data found for {source_folder}")
        return df
    df = select_columns(df, column_mapping, columns_to_use)
    df['SOURCE'] = source_folder # Add a SOURCE column based on the folder name
    print(f'Loaded {source_folder} with {len(df)} rows')
    return df

if __name__ == '__main__':
    
    Envirostor_df = load_and_select(cg.Envirostor_folder, cg.Envirostor_columns_mapping, cg.Envirostor_columns_to_use)

    
    Geotracker_df = load_and_select(cg.Geotracker_folder, cg.Geotracker_columns_mapping, cg.Geotracker_columns_to_use)

    
    combined = pd.concat([Envirostor_df,Geotracker_df], ignore_index=True)
    print(f'Combined dataset has {len(combined)} rows')
    
    