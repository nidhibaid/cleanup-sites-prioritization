import geopandas as gpd
import pandas as pd
import config as cg
from load import load_and_select
import os
import matplotlib.pyplot as plt
import json

# convert pandas dataframe to geodataframe
def df_to_gdf(df, lat_col='LATITUDE', lon_col='LONGITUDE'):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]))
    gdf.set_crs(epsg=4326, inplace=True)  # Set the coordinate reference system to WGS84
    return gdf

# read SMC_AOI GeoJSON file
def load_aoi(aoi_file):
    aoi_gdf = gpd.read_file(aoi_file)
    aoi_gdf.set_crs(epsg=4326, inplace=True)  # Ensure AOI is in WGS84
    print(f'Loaded AOI with {len(aoi_gdf)} features')
    return aoi_gdf

if __name__ == '__main__':
    
    # Load AOI
    aoi_gdf = load_aoi(os.path.join(cg.data_folder, cg.AOI_file))
    aoi_gdf = aoi_gdf[aoi_gdf['JURIS'] == 'EPA']
    print(f'Loaded AOI with {len(aoi_gdf)} features')
    print(aoi_gdf.head())
    
    # Load and select sites from both sources
    Envirostor_df = load_and_select(cg.Envirostor_folder, cg.Envirostor_columns_mapping, cg.Envirostor_columns_to_use)
    Geotracker_df = load_and_select(cg.Geotracker_folder, cg.Geotracker_columns_mapping, cg.Geotracker_columns_to_use)

    # Combine datasets
    combined_df = pd.concat([Envirostor_df, Geotracker_df], ignore_index=True)
    print(f'Combined dataset has {len(combined_df)} rows')

    # Convert to GeoDataFrame and ensure valid geometries
    combined_gdf = df_to_gdf(combined_df)
    combined_gdf = combined_gdf[combined_gdf.geometry.notnull()]
    print(f'Combined geodataframe has {len(combined_gdf)} rows')
    combined_gdf = combined_gdf.to_crs(aoi_gdf.crs)

    # Spatial join to find sites within AOI
    sites_within_aoi = gpd.sjoin(combined_gdf, aoi_gdf, how='inner', predicate='within')
    print(f'Found {len(sites_within_aoi)} sites within the AOI')

    ax = aoi_gdf.plot(color='lightgrey', edgecolor='black', figsize=(20, 20))
    sites_within_aoi.plot(ax=ax, column='SITE_TYPE', categorical=True, markersize=20, legend=True)
    plt.show()
    
    sites_within_aoi.to_csv(os.path.join(cg.data_folder, 'sites_within_aoi.csv'), index=False)
 
# ## EXTRA CODE TO LOAD JURSISDICTIONAL BOUNDARIES
# with open(os.path.join(cg.data_folder,cg.Juris_file)) as f:
#         data = json.load(f)

# # Each item in the array is its own FeatureCollection
# aoi_gdf = gpd.GeoDataFrame(pd.concat([gpd.GeoDataFrame.from_features(fc["features"]) for fc in data], ignore_index=True))
# aoi_gdf.set_crs(epsg=4326, inplace=True)
# aoi_gdf.plot(figsize=(10, 10))
# plt.show()   