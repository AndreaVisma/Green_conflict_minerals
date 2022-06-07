# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import geopandas 
import pandas as pd
import pooch

#%% Import Prio grid (without data)

filepath = "E:\Thesis\Data/priogrid_cell.dbf"
prio_grid = geopandas.read_file(filepath)

print(prio_grid.head())

#%% slice the prio grid shapefile to get only the cells in Africa

file = pooch.retrieve(
    "https://pubs.usgs.gov/of/2006/1187/basemaps/continents/continents.zip", None
)

continents = geopandas.read_file("zip://" + file)

#%%
Africa = continents[continents["CONTINENT"] == "Africa"]

africa_grid = geopandas.sjoin(prio_grid, Africa, how = "right")

prio_africa_grid = prio_grid.iloc[africa_grid.index_left.unique(), :]

ax = prio_africa_grid.plot(markersize=.1, figsize=(12, 8), edgecolor='grey',  facecolor="none")

#%% import temperature data

temp_file = "E:\Thesis\Data/temp.csv"
temp_df = pd.read_csv(temp_file)
temp_df = temp_df[["gid", "temp"]]

#%% merge temperature data with the africa cell grid

temp_grid = pd.merge(prio_africa_grid, temp_df, on = "gid")

#%% plot temperature data in africa

ax = temp_grid.plot(figsize = (12, 9), column = "temp", cmap = "inferno", legend = True)
ax.set_title("average temperature in Africa (2014)")

#%% do the same for South America

SAmerica = continents[continents["CONTINENT"] == "South America"]

SAmerica_grid = geopandas.sjoin(prio_grid, SAmerica, how = "right")

prio_SAmerica_grid = prio_grid.iloc[SAmerica_grid.index_left.unique(), :]

ax = prio_SAmerica_grid.plot(markersize=.1, figsize=(12, 8), edgecolor='grey',  facecolor="none")

SAmerica_temp_grid = pd.merge(prio_SAmerica_grid, temp_df, on = "gid")

ax = SAmerica_temp_grid.plot(figsize = (12, 9), column = "temp", cmap = "inferno", legend = True)
ax.set_title("average temperature in South America (2014)")

#%%

import pandas as pd
import os
import inspect

THIS_FOLDER = os.path.dirname(inspect.getfile(lambda: None))

data_path = "E:\\WPy64-39100\\notebooks\\Thesis_data\\Data_sources\\ged211.csv"

df = pd.read_csv(data_path)

print("datafrme dimensions: ", df.shape)
print("     ")
print(df.head())

df = df[1990 <= df['year']]

violence_dict = {1 : "state_based", 2 : "non_state", 3 : "one_sided"}
df['type_of_violence'].replace(to_replace = violence_dict, inplace=True)

df_Africa = df[df['region'] == 'Africa']
df_Americas = df[df['region'] == 'Americas']
df_Asia = df[df['region'] == 'Asia']

gdf = geopandas.GeoDataFrame(
    df_Africa, geometry=geopandas.points_from_xy(df_Africa.longitude, df_Africa.latitude))

#%%

conflict_grid = geopandas.sjoin(prio_africa_grid, gdf, how = "left", predicate = "contains")
