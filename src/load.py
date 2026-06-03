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

if __name__ == '__main__':
    df = load_sites(cg.Envirostor_folder)
    print(f'Loaded {len(df)} rows')
    print(df.columns.tolist())