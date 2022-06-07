# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:58:04 2022

@author: avism
"""

import geopandas as gpd
import pandas as pd

import os
import inspect

#%%
THIS_FOLDER = os.path.dirname(inspect.getfile(lambda: None))

data_path = "F:\\WPy64-39100\\notebooks\\Thesis_data\\Data_sources\\ged211.csv"

df = pd.read_csv(data_path)

print("datafrme dimensions: ", df.shape)
print("     ")
print(df.head())

#%%
print(df['conflict_name'].isnull().values.sum())

#%% Now some data cleaning and arranging

df = df[1990 <= df['year']]

violence_dict = {1 : "state_based", 2 : "non_state", 3 : "one_sided"}
df['type_of_violence'].replace(to_replace = violence_dict, inplace=True)

df_Africa = df[df['region'] == 'Africa']
df_Americas = df[df['region'] == 'Americas']
df_Asia = df[df['region'] == 'Asia']

#%%

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

#%%

crs_lonlat = ccrs.PlateCarree()
extent_lonlat = [-23, 55, -35, 40] #necessary to get Africa
subplot_kw = dict(projection=crs_lonlat)

cmap = matplotlib.cm.get_cmap('Paired')
color_indexer = np.linspace(0, 1, len(df_Africa['type_of_violence'].unique()))
color_list = cmap(color_indexer)
color_dict = dict(zip(df_Africa['type_of_violence'].unique(), color_list))

df_Africa['color'] = df_Africa['type_of_violence'].map(color_dict)

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)

# plot content 

ax.set_extent(extent_lonlat, crs=crs_lonlat)
ax.coastlines()
ax.stock_img()
ax.add_feature(cfeature.BORDERS)

plt.scatter(x=df_Africa.longitude, y=df_Africa.latitude,
            color= df_Africa.color, edgecolors='black',
            transform=ccrs.PlateCarree()) ## Important

# legend

import matplotlib.patches as mpatches

legend_list = []

for conflict in df_Africa['type_of_violence'].unique():
    
    legend_list.append(mpatches.Patch(color=color_dict[conflict], label=conflict))
    
plt.legend(handles=legend_list)

fig.savefig("F:\\WPy64-39100\\notebooks\\Thesis_data\\Africa_conflict_distribution_1990-2021.pdf")

plt.show()

#%% 

def region_plot(df_here, years, region):
    
    df_here = df_here[years[0] <= df_here['year']]
    df_here = df_here[df_here['year'] <= years[1]]
    
    if region == 'Africa':
        extent_lonlat = [-23, 55, -35, 40] #necessary to get Africa
    elif region == 'Americas':
        extent_lonlat = [-120, -30, -60, 35]
    crs_lonlat = ccrs.PlateCarree()
    subplot_kw = dict(projection=crs_lonlat)

    cmap = matplotlib.cm.get_cmap('Paired')
    color_indexer = np.linspace(0, 1, len(df_here['type_of_violence'].unique()))
    color_list = cmap(color_indexer)
    color_dict = dict(zip(df_here['type_of_violence'].unique(), color_list))

    df['color'] = df_here['type_of_violence'].map(color_dict)

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)

    # plot content 

    ax.set_extent(extent_lonlat, crs=crs_lonlat)
    ax.coastlines()
    ax.stock_img()
    ax.add_feature(cfeature.BORDERS)

    plt.scatter(x=df_here.longitude, y=df_here.latitude,
                color= df_here.color, edgecolors='black',
                transform=ccrs.PlateCarree()) ## Important

    # legend

    import matplotlib.patches as mpatches

    legend_list = []

    for conflict in df_here['type_of_violence'].unique():
        
        legend_list.append(mpatches.Patch(color=color_dict[conflict], label=conflict))
        
    plt.legend(handles=legend_list)

    fig.savefig("F:\\WPy64-39100\\notebooks\\Thesis_data\\" + region +"_conflict_distribution_" 
                + str(years[0]) + "-" + str(years[1]) + ".pdf")

    plt.show()

#%%

region_plot(df_Africa, [2000, 2020], 'Africa')