from osgeo import gdal, osr
import os
from gsflow.output import PrmsDiscretization, PrmsPlot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


def ReprojectCoords(coords,src_srs,tgt_srs):
    """ Reproject a list of x,y coordinates. """
    trans_coords=[]
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)
    for x,y in coords:
        x,y,z = transform.TransformPoint(x,y)
        trans_coords.append([x,y])
    return trans_coords


def lat_lon_labels(axes_, crop_edges=False):
    # if crop_edges:
    #     orig_ylim = axes_.get_ylim()
    #     new_ymin = orig_ylim[0] + 0.2 * (orig_ylim[1] - orig_ylim[0])
    #     new_ymax = orig_ylim[1] - 0.05 * (orig_ylim[1] - orig_ylim[0])
    #     axes_.set_ylim([new_ymin, new_ymax])
    #     orig_xlim = axes_.get_xlim()
    #     new_xmin = orig_xlim[0] + 0.07 * (orig_xlim[1] - orig_xlim[0])
    #     new_xmax = orig_xlim[1] - 0.07 * (orig_xlim[1] - orig_xlim[0])
    #     axes_.set_xlim([new_xmin, new_xmax])
    # else:
    #     orig_ylim = axes_.get_ylim()
    #     new_ymin = orig_ylim[0] + 0.1 * (orig_ylim[1] - orig_ylim[0])
    #     axes_.set_ylim([new_ymin, orig_ylim[1]])
    axes_.set_aspect('equal')
    # now onto the lat lon business
    src_srs = osr.SpatialReference()
    src_srs.ImportFromWkt(ds.GetProjection())
    tgt_srs = src_srs.CloneGeogCS()
    xlabels = axes_.get_xticks()
    ylabels = axes_.get_yticks()
    xlim = axes_.get_xlim()
    ylim = axes_.get_ylim()
    xcoords = [(xlab, ylim[0]) for xlab in xlabels]
    ycoords = [(xlim[0], ylab) for ylab in ylabels]
    new_xcoords = ReprojectCoords(xcoords, src_srs, tgt_srs)
    new_ycoords = ReprojectCoords(ycoords, src_srs, tgt_srs)
    xlons = [-np.round(lon[0], 1) for lon in new_xcoords]
    ylats = [np.round(lat[1], 1) for lat in new_ycoords]
    axes_.set_xticklabels(xlons)
    axes_.set_yticklabels(ylats)
    axes_.set_ylabel('Latitude ($^\circ$N)')
    axes_.set_xlabel('Longitude ($^\circ$W)')
    return axes_



fname = os.path.join('basemap.tif')
img = plt.imread(os.path.join(fname))
# gdal
ds = gdal.Open(fname)
data = ds.ReadAsArray()
gt = ds.GetGeoTransform()
extent = (gt[0], gt[0] + ds.RasterXSize * gt[1],
          gt[3] + ds.RasterYSize * gt[5], gt[3])

workspace = os.path.join('UCRB', 'ucb', 'ucb')

# shp = os.path.join('UCRB', 'HRU_subset.shp')
shp = os.path.join('UCRB', 'MyProject', 'new_projection.shp')
prms_dis = PrmsDiscretization.load_from_shapefile(os.path.join(shp), hru_id='model_idx')
prms_dis.plot_discretization()

irr = pd.read_csv('nhru_summary_ag_irrigation_add.csv', header=0)
irr_dt_format = '%Y-%m-%d'
irr_date_list = np.array([datetime.datetime.strptime(irr['Date'].iloc[i], irr_dt_format) for i, dummy in irr.iterrows()])

start_date = datetime.datetime(2016, 4, 1)
end_date = datetime.datetime(2016, 9, 30)
subset = (start_date <= irr_date_list) & (irr_date_list <= end_date)
irr_data = irr.iloc[subset, 1:]
sum_data = irr_data.sum(axis=0)

fig = plt.figure(figsize=(6, 8))
plt.imshow(img, extent=extent, origin='upper')
plot = PrmsPlot(prms_dis)
ax = plot.plot_array(sum_data, masked_values=[0], cmap='Blues', vmax=30)
axes = plt.gca()
# axes.set_aspect('equal')
# axes.xaxis.set_ticks([])
# axes.yaxis.set_ticks([])
cbar_ax = fig.add_axes([0.85, 0.25, 0.05, 0.5])
cb = plt.colorbar(ax, cax=cbar_ax)
cbar_ax.set_title('Inches\n')
axes = lat_lon_labels(axes)
fig.subplots_adjust(right=0.8)
fig.suptitle('Growing Season 2016\nApplied Irrigation', fontsize=20)
fig.savefig('mapview.png', dpi=500)
