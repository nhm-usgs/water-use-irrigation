#!/usr/bin/env python
# coding: utf-8

# In[1]:


# On mxpwr: conda activate pangeo

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
#%matplotlib inline
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import fiona
import csv

import matplotlib.colors as colors


# In[2]:


gdb_path = './GFv1.1.gdb'
pkwater_equiv_fn = './hru_actet.csv'
base_out_fn = './hru_actet_'


# In[3]:


def get_dim_value(pfn):
    dims = {}
    reading_dims = False
    with open(pfn) as f:
        for line in f:
            line = line.rstrip()  # remove '\n' at end of line
            
            if line == '** Dimensions **':
                reading_dims = True
                f.readline()
            if line == '** Parameters **':
                reading_dims = False
                break
                            
            if reading_dims:
                dim_name = f.readline()
                dim_name = dim_name.rstrip()
                size = f.readline()
                size = size.rstrip()
                dims[dim_name] = int(size)
                            
            if 'str' in line:
                break
    f.close()
    return dims


# In[4]:


def get_param_value(pfn, param_name):
    vals = {}
    reading_vals = False
    with open(pfn) as f:
        for line in f:
            line = line.rstrip()  # remove '\n' at end of line
            
#            print(reading_vals,line,param_name)
            if line == param_name:
                reading_vals = True
                line = f.readline()
                line = line.rstrip()
                num_dims = int(line)
                param_dims = [None] * num_dims
                for ii in range(num_dims):
                    line = f.readline()
                    param_dims[ii] = line.rstrip()
                line = f.readline()
                line = line.rstrip()
                num_vals = int(line)
                line = f.readline()
                line = line.rstrip()
                tp = int(line)
                line = f.readline()
                
                if tp == 2:
                    vals = np.zeros(num_vals, dtype=np.float)
                elif tp == 1:
                    vals = np.zeros(num_vals, dtype=np.int)                    
                jj = 0
                    
            if reading_vals and line == '####':
                reading_vals = False
                break
                            
            if reading_vals:
                val_s = line.rstrip()
                if tp == 2:
                    vals[jj] = float(val_s)
                elif tp == 1:
                    vals[jj] = int(val_s)
                    
                jj += 1
                    
#                size = f.readline()
#                size = size.rstrip()
#                dims[dim_name] = int(size)
#                print(val_s)
                            
            if 'str' in line:
                break
    f.close()
    return vals


# In[5]:


# Get all the layers from the .gdb file
layers = fiona.listlayers(gdb_path)
print(layers)


# In[6]:


gdf = gpd.read_file(gdb_path, layer='nhru_v1_1_simp')


# In[7]:


gdf.head()


# In[8]:


print(gdf.shape)


# In[9]:


with open(pkwater_equiv_fn) as f:
    ncols = len(f.readline().split(','))
    
print(ncols)


# In[10]:


dates = np.loadtxt(pkwater_equiv_fn, delimiter=',',dtype=np.str, skiprows=1, usecols = 0, )
dates = dates.astype('datetime64',copy=True)
#ndates = len(dates)


# In[11]:


vals = np.loadtxt(pkwater_equiv_fn, delimiter=',', dtype=np.float, skiprows=1, usecols=range(1,ncols))


# In[12]:


print(vals.shape)
nhru = vals.shape[1]


# In[13]:


print(vals.shape)
print(nhru)


# In[14]:


df = pd.DataFrame(list(range(1, nhru+1)), columns=['$id'])


# In[15]:


date_idx = 455
print(dates)
print(dates[date_idx])
pkwater_equiv_vals = vals[date_idx,:]


# In[16]:


foobar = np.zeros(len(pkwater_equiv_vals), dtype=np.float)
limit = 0.01
for ii in range(len(pkwater_equiv_vals)):
    if pkwater_equiv_vals[ii] > limit:
        foobar[ii] = np.log(pkwater_equiv_vals[ii])
    else:
        foobar[ii] = np.log(limit)

df["pkwater_equiv"] = foobar
df.head()


# In[17]:


print(df.shape)


# In[18]:


try:
    gdf = gdf.drop(columns=['pkwater_equiv'])
except:
    pass
    
gdf = gdf.join(df.set_index('$id'), on='nhru_v11')


# In[19]:


gdf.head()


# In[ ]:


for date_idx in range(0, len(dates)):
    pkwater_equiv_vals = vals[date_idx,:]
    print(pkwater_equiv_vals)
    print(min(pkwater_equiv_vals), max(pkwater_equiv_vals))

    foobar = np.zeros(len(pkwater_equiv_vals), dtype=np.float)
    limit = 0.01
#    for ii in range(len(pkwater_equiv_vals)):
#        if pkwater_equiv_vals[ii] > limit:
#            foobar[ii] = np.log(pkwater_equiv_vals[ii])
#        else:
#            foobar[ii] = np.log(limit)

    for ii in range(len(pkwater_equiv_vals)):
        if pkwater_equiv_vals[ii] > limit:
#            foobar[ii] = np.log10(pkwater_equiv_vals[ii])
            foobar[ii] = pkwater_equiv_vals[ii]
        else:
#            foobar[ii] = np.log10(limit)
            foobar[ii] = limit

    df["pkwater_equiv"] = foobar

    try:
        gdf = gdf.drop(columns=['pkwater_equiv'])
    except:
        pass

    gdf = gdf.join(df.set_index('$id'), on='nhru_v11')

    # plot the seg_outflow values

    # plot all HRUs in white (background color)
    #f, ax = plt.subplots(1, figsize=(12, 12))
    fig, ax = plt.subplots(1, figsize=(12, 12))
    #hrus.plot(color="white", ax=ax)

    gdf.plot(column='pkwater_equiv', cmap='coolwarm', ax=ax, edgecolor="face", norm=colors.LogNorm(vmin=limit, vmax=max(pkwater_equiv_vals)))

    ax.axis('off')
    # add a title
    ax.set_title('pkwater_equiv: ' + str(dates[date_idx])[:10], fontdict={'fontsize': '25', 'fontweight' : '3'})
    # create an annotation for the data source
    ax.annotate('ONHM, PRMS v5.1.0, GFv1.1, Units: inches',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left',
                verticalalignment='top', fontsize=12, color='#555555')

    # df.dropna(thresh=2)

    # Create colorbar as a legend
    #sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=min(foobar), vmax=max(foobar)))
# https://matplotlib.org/tutorials/colors/colormapnorms.html
#    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=colors.LogNorm(vmin=min(np.log10(pkwater_equiv_vals)), vmax=max(np.log10(pkwater_equiv_vals))))
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=colors.LogNorm(vmin=limit, vmax=max(pkwater_equiv_vals)))
#    norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),

    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    cbar = fig.colorbar(sm)

    fn_new = base_out_fn + '{:04d}'.format(date_idx) + '.png'
    fig.savefig(fn_new, dpi=100)
    
    plt.cla()
    plt.clf()
    plt.close('all')


# In[ ]:
