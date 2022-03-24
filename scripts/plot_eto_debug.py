import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
import calendar
import os 

out_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/test_model/prms/projects/ucb_daily_ag_frac_transp/output/'

hru_list = [84078, 84427, 85751, 83371, 84738, 84965]  # nhru_v11 (not nhm_id)
hru_name = ['Delta', 'Fruita', 'Vernal', 'Durango', 'Kremmling', 'Kirtland']
desc = [' (West Central Colorado)', ' (West Central Colorado)', ' (Northeast Utah)', ' (Southwest Colorado)', ' (North Central Colorado)', ' (Northwest New Mexico)']

# get key to convert nhm_id to model_idx:
idx_key = pd.read_csv('idx_to_nhru.csv', header=0)
# Irrigated Area (acres):
hru_areas = pd.read_csv('hru_area.csv', header=0)
ag_fracs = pd.read_csv('ia_2016_ucb.csv', header=0)

dt_format = '%Y-%m-%d'
# potential ET (from NHM/PRMS)
potet = pd.read_csv(os.path.join(out_dir, 'nhru_summary_potet.csv'))
potet.columns = [str(c) for c in range(len(potet.columns))]
potet_date_list = np.array([datetime.datetime.strptime(potet['0'].iloc[i], dt_format) for i, dummy in potet.iterrows()])

start_date = datetime.datetime(2015, 10, 1)
end_date = datetime.datetime(2016, 9, 30)
days = (end_date - start_date).days + 1
plot_date_list = [start_date + datetime.timedelta(days=d) for d in range(days)]

# OpenET from output files
eto2 = pd.read_csv(os.path.join(out_dir, 'nhru_summary_PET_external.csv'))
eto2.columns = [str(c) for c in range(len(eto2.columns))]
eto2_date_list = np.array([datetime.datetime.strptime(eto2['0'].iloc[i], dt_format) for i, dummy in eto2.iterrows()])

fig, axes = plt.subplots(2, 3, figsize=(13.33, 7.5))
axes = axes.flat
for num, hru in enumerate(hru_name):
    idx_from_hru = str(idx_key['model_idx'][idx_key['nhru_v11'] == hru_list[num]].item())
    hru_area = hru_areas['hru_area'][int(idx_from_hru)-1]
    ag_frac = ag_fracs['MEAN'][int(idx_from_hru)-1]
    potet_data = potet[idx_from_hru][(start_date <= potet_date_list) & (potet_date_list <= end_date)]
    eto2_data = eto2[idx_from_hru][(start_date <= eto2_date_list) & (eto2_date_list <= end_date)]
    axes[num].plot(plot_date_list, eto2_data, label='ETo (OpenET)', color='tab:orange')
    axes[num].plot(plot_date_list, potet_data, label='potet', color='tab:red')
    if num == 0:
        handles, labels = axes[num].get_legend_handles_labels()
    axes_dates = [calendar.month_name[i][0:3] for i in [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    axes[num].set_xticks(np.arange(mpl_dates.date2num(start_date), mpl_dates.date2num(end_date), 30.42))
    axes[num].set_xticklabels(axes_dates, rotation=-30, ha='left')
    axes[num].set_title(hru + desc[num] + '\nIrrigated Fraction: ' + str(np.round(ag_frac, 2)))
    if (num == 0) or (num == 3):
        axes[num].set_ylabel('Inches\nper\nDay', ha='right', va='center', ma='left', rotation=0)
fig.legend(handles, labels)
fig.tight_layout()
fig.suptitle('Water Year 2016 ETo Comparison', fontsize=20)
fig.subplots_adjust(top=0.86)
fig.savefig('ETo_debug.png', dpi=500)

