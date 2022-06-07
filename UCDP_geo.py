# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:04:23 2022

@author: avism
"""

import pandas as pd
import geopandas as gpd
import os
import inspect

#%%
THIS_FOLDER = os.path.dirname(inspect.getfile(lambda: None))

data_path = "F:\\WPy64-39100\\notebooks\\Thesis_data\\Data_sources\\ged211.csv"

df = pd.read_csv(data_path)

print("datafrme dimensions: ", df.shape)
print("     ")
print(df.head())

#%% Now some data cleaning and arranging

df = df[1990 <= df['year']]

violence_dict = {1 : "state_based", 2 : "non_state", 3 : "one_sided"}
df['type_of_violence'].replace(to_replace = violence_dict, inplace=True)

df_Africa = df[df['region'] == 'Africa']
df_Americas = df[df['region'] == 'Americas']
df_Asia = df[df['region'] == 'Asia']

#%% Import the dataframe into geopandas

import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np

gdf = gpd.GeoDataFrame(
    df_Africa, geometry=gpd.points_from_xy(df_Africa.longitude, df_Africa.latitude))

xmin, ymin, xmax, ymax = gdf.total_bounds

wide = 0.5
length = 0.5

cols = list(np.arange(xmin, xmax + wide, wide))
rows = list(np.arange(ymin, ymax + length, length))

polygons = []
for x in cols[:-1]:
    for y in rows[:-1]:
        polygons.append(Polygon([(x,y), (x+wide, y), (x+wide, y+length), (x, y+length)]))

grid = gpd.GeoDataFrame({'geometry':polygons})
grid.to_file("grid.shp")

#%% 
import matplotlib.pyplot as plt

ax = gdf.plot(markersize=.1, figsize=(12, 8))
plt.autoscale(False)
grid.plot(ax=ax, facecolor="none", edgecolor='grey')
ax.axis("off")

#%%
merged = gpd.sjoin(gdf, grid, how='left', predicate='within')

# make a simple count variable that we can sum
merged.rename(columns = {'index_right':'grid_id'}, inplace=True)
merged['conflicts']=1
# Compute stats per grid cell -- aggregate fires to grid cells with dissolve
dissolve = merged.dissolve(by="grid_id", aggfunc="count")
# put this into cell
grid['conflicts'] = 0
grid.loc[dissolve.index, 'conflicts'] = dissolve.conflicts.values

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

ax = grid.plot(column='conflicts', figsize=(12, 8), cmap='viridis', vmin = 1, edgecolor="grey")
plt.autoscale(False)
world.plot(ax=ax, color='none', edgecolor='black')
ax.axis('off')

plt.savefig("F:\\WPy64-39100\\notebooks\\Thesis_data\\grid.pdf")

#%%

import pooch
import regionmask
