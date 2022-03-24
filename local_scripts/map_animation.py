from osgeo import gdal, osr
import os
from gsflow.output import PrmsDiscretization, PrmsPlot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import calendar
import matplotlib.animation as manimation


def ReprojectCoords(coords,src_srs,tgt_srs):
    """ Reproject a list of x,y coordinates. """
    trans_coords=[]
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)
    for x,y in coords:
        x,y,z = transform.TransformPoint(x,y)
        trans_coords.append([x,y])
    return trans_coords


def lat_lon_labels(axes_):
    axes_.set_aspect('equal')
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
    axes_.set_xticks(axes_.get_xticks()[1:-1])
    axes_.set_yticks(axes_.get_yticks()[1:-1])
    axes_.set_xticklabels(xlons[1:-1])
    axes_.set_yticklabels(ylats[1:-1])
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


# first, calculate never irrigated for masking array:
begin_irr = datetime.datetime(2000, 1, 1)
end_irr = datetime.datetime(2016, 9, 30)
irr_subset = (begin_irr <= irr_date_list) & (irr_date_list <= end_irr)
irr_data = irr.iloc[irr_subset, 1:]
sum_irr = irr_data.sum(axis=0)
mask_array = sum_irr == 0


fig = plt.figure(figsize=(6, 8))
plt.imshow(img, extent=extent, origin='upper')
axes = plt.gca()
axes = lat_lon_labels(axes)
FFMpegWriter = manimation.writers['ffmpeg']
writer = FFMpegWriter(fps=2)
plotted_leg = False
with writer.saving(fig, os.path.join('irrigation_animation.mp4'), dpi=500):
    for year in range(2000, 2016):
        print('processing ' + str(year) + '...')
        for month in range(12):
            start_date = datetime.datetime(year, month+1, 1)
            dummy, days_in_month = calendar.monthrange(year, month+1)
            end_date = datetime.datetime(year, month+1, days_in_month)
            subset = (start_date <= irr_date_list) & (irr_date_list <= end_date)
            irr_data = irr.iloc[subset, 1:]
            sum_data = irr_data.sum(axis=0)
            plot = PrmsPlot(prms_dis)
            # ax = plot.plot_array(mean_data, masked_values=[0], cmap='Blues', vmin=0.0, vmax=0.2, ax=axes)
            masked_hrus = np.ma.masked_where(mask_array, sum_data)
            # ax = plot.plot_array(mean_data, cmap='Blues', vmin=0.0, vmax=0.2, ax=axes)
            ax = plot.plot_array(masked_hrus, cmap='Blues', vmin=0.0, vmax=8, ax=axes)
            if not plotted_leg:
                cbar_ax = fig.add_axes([0.85, 0.25, 0.05, 0.5])
                cb = plt.colorbar(ax, cax=cbar_ax)
                cbar_ax.set_title('Inches\nper Month\n')
                fig.subplots_adjust(right=0.8)
                plotted_leg = True
            month_name = calendar.month_name[month+1]
            fig.suptitle('Mean Daily Applied Irrigation Estimate:\n' + month_name + ' ' + str(year), fontsize=20)
            writer.grab_frame()
