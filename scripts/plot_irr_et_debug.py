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

# "net precip" (precip that makes it past canopy)
ppt = pd.read_csv(os.path.join(out_dir, 'nhru_summary_net_ppt.csv'))
ppt.columns = [str(c) for c in range(len(ppt.columns))]
ppt_date_list = np.array([datetime.datetime.strptime(ppt['0'].iloc[i], dt_format) for i, dummy in ppt.iterrows()])

# actual ET (from NHM/PRMS)
actet = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_actet.csv'))
actet.columns = [str(c) for c in range(len(actet.columns))]
actet_date_list = np.array([datetime.datetime.strptime(actet['0'].iloc[i], dt_format) for i, dummy in actet.iterrows()])

# applied irrigation (from NHM/PRMS)
irr = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_irrigation_add.csv'))
irr.columns = [str(c) for c in range(len(irr.columns))]
irr_date_list = np.array([datetime.datetime.strptime(irr['0'].iloc[i], dt_format) for i, dummy in irr.iterrows()])

# potential ET (from NHM/PRMS)
potet = pd.read_csv(os.path.join(out_dir, 'nhru_summary_potet.csv'))
potet.columns = [str(c) for c in range(len(actet.columns))]
potet_date_list = np.array([datetime.datetime.strptime(potet['0'].iloc[i], dt_format) for i, dummy in potet.iterrows()])

# soil moisture
moist = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_soil_rechr.csv'))  # moist.csv'))
moist.columns = [str(c) for c in range(len(moist.columns))]
moist_date_list = np.array([datetime.datetime.strptime(moist['0'].iloc[i], dt_format) for i, dummy in moist.iterrows()])

start_date = datetime.datetime(2016, 4, 1)
end_date = datetime.datetime(2016, 9, 30)
days = (end_date - start_date).days + 1
plot_date_list = [start_date + datetime.timedelta(days=d) for d in range(days)]

# OpenET from output files
et2 = pd.read_csv(os.path.join(out_dir, 'nhru_summary_AET_external.csv'))
et2.columns = [str(c) for c in range(len(et2.columns))]
et2_date_list = np.array([datetime.datetime.strptime(et2['0'].iloc[i], dt_format) for i, dummy in et2.iterrows()])

eto2 = pd.read_csv(os.path.join(out_dir, 'nhru_summary_PET_external.csv'))
eto2.columns = [str(c) for c in range(len(eto2.columns))]
eto2_date_list = np.array([datetime.datetime.strptime(eto2['0'].iloc[i], dt_format) for i, dummy in eto2.iterrows()])

fig, axes = plt.subplots(2, 3, figsize=(13.33, 7.5))
axes = axes.flat
for num, hru in enumerate(hru_name):
    idx_from_hru = str(idx_key['model_idx'][idx_key['nhru_v11'] == hru_list[num]].item())
    hru_area = hru_areas['hru_area'][int(idx_from_hru)-1]
    ag_frac = ag_fracs['MEAN'][int(idx_from_hru)-1]
    actet_data = actet[idx_from_hru][(start_date <= actet_date_list) & (actet_date_list <= end_date)]
    potet_data = potet[idx_from_hru][(start_date <= potet_date_list) & (potet_date_list <= end_date)]
    et2_data = et2[idx_from_hru][(start_date <= et2_date_list) & (et2_date_list <= end_date)]
    eto2_data = eto2[idx_from_hru][(start_date <= eto2_date_list) & (eto2_date_list <= end_date)]
    irr_data = irr[idx_from_hru][(start_date <= irr_date_list) & (irr_date_list <= end_date)]
    ppt_data = ppt[idx_from_hru][(start_date <= ppt_date_list) & (ppt_date_list <= end_date)]
    moist_data = moist[idx_from_hru][(start_date <= moist_date_list) & (moist_date_list <= end_date)]
    ax2 = axes[num].twinx()
    ax2.plot(plot_date_list, np.nancumsum(et2_data), label='ETa (OpenET)', color='tab:blue')
    ax2.plot(plot_date_list, np.nancumsum(actet_data), label='ag_actet', color='tab:green')
    ax2.plot(plot_date_list, np.nancumsum(irr_data), label='ag_irrigation_add', color='tab:purple')
    ax2.plot(plot_date_list, np.nancumsum(ppt_data), label='net_ppt', color='tab:pink')
    axes[num].fill_between(x=plot_date_list, y1=moist_data, label='Capillary Storage', alpha=0.3, color='tab:gray')
    if num == 0:
        handles1, labels1 = axes[num].get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles = handles1 + handles2
        labels = labels1 + labels2
    axes_dates = [calendar.month_name[i][0:3] for i in [4, 5, 6, 7, 8, 9]]
    axes[num].set_xticks(np.arange(mpl_dates.date2num(start_date), mpl_dates.date2num(end_date), 30.42))
    axes[num].set_xticklabels(axes_dates, rotation=-30, ha='left')
    ax2.set_title(hru + desc[num] + '\nIrrigated Fraction: ' + str(np.round(ag_frac, 2)))
    if (num == 2) or (num == 5):
        ax2.set_ylabel('Cumulative\nInches', rotation=0, ma='left', ha='left')  #, ha='right', va='center', ma='left', rotation=0)
    ax2.set_ylim([0, 32])
    if (num == 0) or (num == 3):
        axes[num].set_ylabel('Capillary\nStorage\n(Inches)', ha='right', va='center', ma='left', rotation=0)
    axes[num].set_ylim([0, 3.2])

fig.legend(handles, labels)
fig.tight_layout()
fig.suptitle('Growing Season 2016 Cumulative ET,\nPrecipitation, and Irrigation', fontsize=20)
fig.subplots_adjust(top=0.8)
fig.savefig('ET_irr_debug.png', dpi=500)

