import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
import calendar
import os 

out_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/test_model/prms/projects/ucb/output/'
hru_list = [84078, 84427, 85751, 83371, 84738, 84965]  # nhru_v11 (not nhm_id)
hru_name = ['Delta', 'Fruita', 'Vernal', 'Durango', 'Kremmling', 'Kirtland']
desc = [' (West Central Colorado)', ' (West Central Colorado)', ' (Northeast Utah)', ' (Southwest Colorado)', ' (North Central Colorado)', ' (Northwest New Mexico)']

# get key to convert nhm_id to model_idx:
idx_key = pd.read_csv('idx_to_nhru.csv', header=0)
# Irrigated Area (acres):
hru_areas = pd.read_csv('hru_area.csv', header=0)
ag_fracs = pd.read_csv('ia_2016_ucb.csv', header=0)

dt_format = '%Y-%m-%d'
# applied irrigation (from NHM/PRMS)
irr = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_irrigation_add.csv'))
irr.columns = [str(c) for c in range(len(irr.columns))]
irr_date_list = np.array([datetime.datetime.strptime(irr['0'].iloc[i], dt_format) for i, dummy in irr.iterrows()])

# applied irrigation (from NHM/PRMS)
irr_vol = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_irrigation_add_vol.csv'))
irr_vol.columns = [str(c) for c in range(len(irr_vol.columns))]
irr_vol_date_list = np.array([datetime.datetime.strptime(irr_vol['0'].iloc[i], dt_format) for i, dummy in irr_vol.iterrows()])

# runoff (from NHM/PRMS)
runoff = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_hortonian.csv'))
runoff.columns = [str(c) for c in range(len(runoff.columns))]
runoff_date_list = np.array([datetime.datetime.strptime(runoff['0'].iloc[i], dt_format) for i, dummy in runoff.iterrows()])

# percolation (from NHM/PRMS)
perc = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_soil2gvr.csv'))
perc.columns = [str(c) for c in range(len(perc.columns))]
perc_date_list = np.array([datetime.datetime.strptime(perc['0'].iloc[i], dt_format) for i, dummy in perc.iterrows()])

start_date = datetime.datetime(2015, 10, 1)
end_date = datetime.datetime(2016, 9, 30)
days = (end_date - start_date).days + 1
plot_date_list = [start_date + datetime.timedelta(days=d) for d in range(days)]

fig, axes = plt.subplots(2, 3, figsize=(13.33, 7.5))
axes = axes.flat
for num, hru in enumerate(hru_name):
    idx_from_hru = str(idx_key['model_idx'][idx_key['nhru_v11'] == hru_list[num]].item())
    hru_area = hru_areas['hru_area'][int(idx_from_hru)-1]
    ag_frac = ag_fracs['MEAN'][int(idx_from_hru)-1]
    irr_area = hru_area * ag_frac
    irr_data = irr[idx_from_hru][(start_date <= irr_date_list) & (irr_date_list <= end_date)]
    irr_vol_data = irr_vol[idx_from_hru][(start_date <= irr_vol_date_list) & (irr_vol_date_list <= end_date)]
    runoff_data = runoff[idx_from_hru][(start_date <= runoff_date_list) & (runoff_date_list <= end_date)]
    perc_data = perc[idx_from_hru][(start_date <= perc_date_list) & (perc_date_list <= end_date)]
    axes[num].plot(plot_date_list, np.nancumsum(irr_data), label='Applied Irrigation', color='tab:purple')
    #axes[num].plot(plot_date_list, np.nancumsum(irr_vol_data / irr_area), label='Applied Irrigation\n(model output in acre inches\ndivided by irrigated area)', color='tab:pink')
    axes[num].plot(plot_date_list, np.nancumsum(runoff_data), label='Runoff', color='tab:cyan')
    axes[num].plot(plot_date_list, np.nancumsum(perc_data), label='Percolation', color='tab:brown')
    if num == 0:
        handles, labels = axes[num].get_legend_handles_labels()
    axes_dates = [calendar.month_name[i][0:3] for i in [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    axes[num].set_xticks(np.arange(mpl_dates.date2num(start_date), mpl_dates.date2num(end_date), 30.42))
    axes[num].set_xticklabels(axes_dates, rotation=-30, ha='left')
    axes[num].set_title(hru + desc[num] + '\nIrrigated Fraction: ' + str(np.round(ag_frac, 2)))
    if (num == 0) or (num == 3):
        axes[num].set_ylabel('Inches', ha='right', va='center', ma='left', rotation=0)

fig.legend(handles, labels)
fig.tight_layout()
fig.suptitle('WY2016 Cumulative Applied Irrigation, Runoff, and Deep Percolation:\nUpper Colorado River Basin', fontsize=20)
fig.subplots_adjust(top=0.8)
fig.savefig('irr_runoff.png', dpi=500)

