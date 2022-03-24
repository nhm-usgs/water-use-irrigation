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
snow_evap = pd.read_csv(os.path.join(out_dir, 'nhru_summary_snow_evap.csv'))
snow_evap.columns = [str(c) for c in range(len(snow_evap.columns))]
snow_evap_date_list = np.array([datetime.datetime.strptime(snow_evap['0'].iloc[i], dt_format) for i, dummy in snow_evap.iterrows()])

hru_intcpevap = pd.read_csv(os.path.join(out_dir, 'nhru_summary_hru_intcpevap.csv'))
hru_intcpevap.columns = [str(c) for c in range(len(hru_intcpevap.columns))]
hru_intcpevap_date_list = np.array([datetime.datetime.strptime(hru_intcpevap['0'].iloc[i], dt_format) for i, dummy in hru_intcpevap.iterrows()])

dprst_evap = pd.read_csv(os.path.join(out_dir, 'nhru_summary_dprst_evap_hru.csv'))
dprst_evap.columns = [str(c) for c in range(len(dprst_evap.columns))]
dprst_evap_date_list = np.array([datetime.datetime.strptime(dprst_evap['0'].iloc[i], dt_format) for i, dummy in dprst_evap.iterrows()])

hru_impervevap = pd.read_csv(os.path.join(out_dir, 'nhru_summary_hru_impervevap.csv'))
hru_impervevap.columns = [str(c) for c in range(len(hru_impervevap.columns))]
hru_impervevap_date_list = np.array([datetime.datetime.strptime(hru_impervevap['0'].iloc[i], dt_format) for i, dummy in hru_impervevap.iterrows()])

perv_actet = pd.read_csv(os.path.join(out_dir, 'nhru_summary_hru_perv_actet.csv'))
perv_actet.columns = [str(c) for c in range(len(perv_actet.columns))]
perv_actet_date_list = np.array([datetime.datetime.strptime(perv_actet['0'].iloc[i], dt_format) for i, dummy in perv_actet.iterrows()])

hru_ag_actet = pd.read_csv(os.path.join(out_dir, 'nhru_summary_hru_ag_actet.csv'))
hru_ag_actet.columns = [str(c) for c in range(len(hru_ag_actet.columns))]
hru_ag_actet_date_list = np.array([datetime.datetime.strptime(hru_ag_actet['0'].iloc[i], dt_format) for i, dummy in hru_ag_actet.iterrows()])

# soil moisture
moist = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_soil_rechr.csv'))  # moist.csv'))
moist.columns = [str(c) for c in range(len(moist.columns))]
moist_date_list = np.array([datetime.datetime.strptime(moist['0'].iloc[i], dt_format) for i, dummy in moist.iterrows()])

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
    snow_evap_data = snow_evap[idx_from_hru][(start_date <= snow_evap_date_list) & (snow_evap_date_list <= end_date)]
    hru_intcpevap_data = hru_intcpevap[idx_from_hru][(start_date <= hru_intcpevap_date_list) & (hru_intcpevap_date_list <= end_date)]
    dprst_evap_data = dprst_evap[idx_from_hru][(start_date <= dprst_evap_date_list) & (dprst_evap_date_list <= end_date)]
    hru_impervevap_data = hru_impervevap[idx_from_hru][(start_date <= hru_impervevap_date_list) & (hru_impervevap_date_list <= end_date)]
    perv_actet_data = perv_actet[idx_from_hru][(start_date <= perv_actet_date_list) & (perv_actet_date_list <= end_date)]
    hru_ag_actet_data = hru_ag_actet[idx_from_hru][(start_date <= hru_ag_actet_date_list) & (hru_ag_actet_date_list <= end_date)]
    moist_data = moist[idx_from_hru][(start_date <= moist_date_list) & (moist_date_list <= end_date)]
    ax2 = axes[num].twinx()
    ax2.plot(plot_date_list, snow_evap_data, label='snow_evap')
    ax2.plot(plot_date_list, hru_intcpevap_data, label='intcpevap')
    ax2.plot(plot_date_list, dprst_evap_data, label='dprst_evap')
    ax2.plot(plot_date_list, hru_impervevap_data, label='impervevap')
    ax2.plot(plot_date_list, perv_actet_data, label='perv_actet')
    ax2.plot(plot_date_list, hru_ag_actet_data, label='ag_actet')
    axes[num].fill_between(x=plot_date_list, y1=moist_data, label='Capillary Storage', alpha=0.3, color='tab:gray')
    if num == 0:
        handles1, labels1 = axes[num].get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles = handles1 + handles2
        labels = labels1 + labels2
    axes_dates = [calendar.month_name[i][0:3] for i in [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    axes[num].set_xticks(np.arange(mpl_dates.date2num(start_date), mpl_dates.date2num(end_date), 30.42))
    axes[num].set_xticklabels(axes_dates, rotation=-30, ha='left')
    ax2.set_title(hru + desc[num] + '\nIrrigated Fraction: ' + str(np.round(ag_frac, 2)))
    if (num == 2) or (num == 5):
        ax2.set_ylabel('Cumulative\nInches', rotation=0, ma='left', ha='left')  #, ha='right', va='center', ma='left', rotation=0)
    ax2.set_ylim([0, 0.22])
    if (num == 0) or (num == 3):
        axes[num].set_ylabel('Capillary\nStorage\n(Inches)', ha='right', va='center', ma='left', rotation=0)
    axes[num].set_ylim([0, 3.2])

fig.legend(handles, labels,ncol=2)
fig.tight_layout()
fig.suptitle('WY2016 Evaporation Fluxes', fontsize=20)
fig.subplots_adjust(top=0.8)
fig.savefig('evap.png', dpi=500)

