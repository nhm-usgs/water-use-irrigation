import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
import calendar

hru_list = [84078, 84427, 85751, 83371, 84738, 84965]  # nhru_v11 (not nhm_id)
hru_name = ['Delta', 'Fruita', 'Vernal', 'Durango', 'Kremmling', 'Kirtland']
desc = [' (West Central Colorado)', ' (West Central Colorado)', ' (Northeast Utah)', ' (Southwest Colorado)', ' (North Central Colorado)', ' (Northwest New Mexico)']

# get key to convert nhm_id to model_idx:
idx_key = pd.read_csv('idx_to_nhru.csv', header=0)
# Irrigated Area (acres):
hru_areas = pd.read_csv('hru_area.csv', header=0)
ag_fracs = pd.read_csv('ia_2016_ucb.csv', header=0)

# applied irrigation (from NHM/PRMS)
irr = pd.read_csv('nhru_summary_ag_irrigation_add.csv')
irr.columns = [str(c) for c in range(len(irr.columns))]
irr_dt_format = '%Y-%m-%d'
irr_date_list = np.array([datetime.datetime.strptime(irr['0'].iloc[i], irr_dt_format) for i, dummy in irr.iterrows()])

# applied irrigation (from NHM/PRMS)
irr_vol = pd.read_csv('nhru_summary_ag_irrigation_add_vol.csv')
irr_vol.columns = [str(c) for c in range(len(irr_vol.columns))]
irr_vol_dt_format = '%Y-%m-%d'
irr_vol_date_list = np.array([datetime.datetime.strptime(irr_vol['0'].iloc[i], irr_vol_dt_format) for i, dummy in irr_vol.iterrows()])

# actual ET (from NHM/PRMS)
actet = pd.read_csv('nhru_summary_ag_actet.csv')
actet.columns = [str(c) for c in range(len(actet.columns))]
actet_dt_format = '%Y-%m-%d'
actet_date_list = np.array([datetime.datetime.strptime(actet['0'].iloc[i], actet_dt_format) for i, dummy in actet.iterrows()])

# potential ET (from NHM/PRMS)
potet = pd.read_csv('nhru_summary_potet.csv')
potet.columns = [str(c) for c in range(len(actet.columns))]
potet_dt_format = '%Y-%m-%d'
potet_date_list = np.array([datetime.datetime.strptime(potet['0'].iloc[i], potet_dt_format) for i, dummy in potet.iterrows()])

# OpenET:
et = pd.read_csv('2016_eta_USGS.csv', header=0)
et_dt_format = '%Y-%m-%d'
et_date_list = np.array([datetime.datetime.strptime(et['time'].iloc[i], et_dt_format) for i, dummy in et.iterrows()])
eto = pd.read_csv('2016_eto_USGS.csv', header=0)
eto_dt_format = '%Y-%m-%d'
eto_date_list = np.array([datetime.datetime.strptime(eto['time'].iloc[i], eto_dt_format) for i, dummy in eto.iterrows()])

start_date = datetime.datetime(2016, 1, 1)
end_date = datetime.datetime(2016, 9, 30)
days = (end_date - start_date).days + 1
plot_date_list = [start_date + datetime.timedelta(days=d) for d in range(days)]

# OpenET from output files
et2 = pd.read_csv('nhru_summary_AET_external.csv')
et2.columns = [str(c) for c in range(len(et2.columns))]
et2_dt_format = '%Y-%m-%d'
et2_date_list = np.array([datetime.datetime.strptime(et2['0'].iloc[i], et2_dt_format) for i, dummy in et2.iterrows()])

eto2 = pd.read_csv('nhru_summary_PET_external.csv')
eto2.columns = [str(c) for c in range(len(eto2.columns))]
eto2_dt_format = '%Y-%m-%d'
eto2_date_list = np.array([datetime.datetime.strptime(eto2['0'].iloc[i], et2_dt_format) for i, dummy in eto2.iterrows()])

fig, axes = plt.subplots(2, 3, figsize=(13.33, 7.5))
axes = axes.flat
for num, hru in enumerate(hru_name):
    idx_from_hru = str(idx_key['model_idx'][idx_key['nhru_v11'] == hru_list[num]].item())
    hru_area = hru_areas['hru_area'][int(idx_from_hru)-1]
    ag_frac = ag_fracs['MEAN'][int(idx_from_hru)-1]
    irr_area = hru_area * ag_frac
    irr_data = irr[idx_from_hru][(start_date <= irr_date_list) & (irr_date_list <= end_date)]
    irr_vol_data = irr_vol[idx_from_hru][(start_date <= irr_vol_date_list) & (irr_vol_date_list <= end_date)]
    actet_data = actet[idx_from_hru][(start_date <= actet_date_list) & (actet_date_list <= end_date)]
    potet_data = potet[idx_from_hru][(start_date <= potet_date_list) & (potet_date_list <= end_date)]
    et2_data = et2[idx_from_hru][(start_date <= et2_date_list) & (et2_date_list <= end_date)]
    eto2_data = eto2[idx_from_hru][(start_date <= eto2_date_list) & (eto2_date_list <= end_date)]
    et_data = np.zeros(len(irr_data))
    eto_data = np.zeros(len(irr_data))
    for i, dt in enumerate(plot_date_list):
        data_date = datetime.datetime(dt.year, dt.month, 1)
        dummy, days_in_month = calendar.monthrange(dt.year, dt.month)
        if np.any(et['mean'][(et['nhm_id'] == int(hru_list[num] + 1)) & (et_date_list == data_date)]):
            acreage = np.mean(et['area'][(et['nhm_id'] == int(hru_list[num] + 1)) & (et_date_list == data_date)])
            et_data[i] = np.mean(et['mean'][(et['nhm_id'] == int(hru_list[num] + 1)) & (et_date_list == data_date)]) / days_in_month * 0.0393701
        if np.any(et['mean'][(et['nhm_id'] == int(hru_list[num] + 1)) & (et_date_list == data_date)]):
            eto_data[i] = np.mean(eto['mean'][(eto['nhm_id'] == int(hru_list[num] + 1)) & (eto_date_list == data_date)]) / days_in_month * 0.0393701
    axes[num].plot(plot_date_list, et2_data, label='ETa (OpenET)')
    axes[num].plot(plot_date_list, eto2_data, label='ETo (OpenET)')
    axes[num].plot(plot_date_list, actet_data, label='ETa (NHM/PRMS')
    axes[num].plot(plot_date_list, potet_data, label='ETo (NHM/PRMS')
    # axes[num].plot(plot_date_list, irr_data, label='Applied Irrigation\n(model output in inches)')
    # axes[num].plot(plot_date_list, irr_vol_data / irr_area, label='Applied Irrigation\n(model output in acre inches\ndivided by irrigated area)', color='tab:pink')
    # print('\n' + hru)
    # print((irr_data / irr_area) / eto2_data)
    if num == 0:
        handles, labels = axes[num].get_legend_handles_labels()
    print(mpl_dates.date2num(start_date))
    print(mpl_dates.date2num(end_date))
    axes_dates = [' ' + calendar.month_name[i+1][0:3] for i in range(9)]
    print(axes[num].get_xlim())
    print(axes[num].get_xticks()[0:9])
    print(axes[num].get_xticks())
    axes[num].set_xticks(axes[num].get_xticks()[0:9])
    axes[num].set_xticklabels(axes_dates, rotation=45, ha='left')
    axes[num].set_title(hru + desc[num] + '\nIrrigated Fraction: ' + str(np.round(ag_frac, 2)))
    if (num == 0) or (num == 3):
        axes[num].set_ylabel('Inches\nper\nDay', ha='right', va='center', ma='left', rotation=0)
    axes[num].set_ylim([0, 0.26])
    # axes[num].set_ylim([0, 100])
# fig.legend(handles[4:6], labels[4:6])
fig.legend(handles, labels)
fig.tight_layout()
# fig.suptitle('2016 ET:\nUpper Colorado River Basin', fontsize=20)
fig.suptitle('2016 Irrigation Estimates using OpenET:\nUpper Colorado River Basin', fontsize=20)
#fig.subplots_adjust(top=0.85)
fig.subplots_adjust(top=0.8)
fig.savefig('irrigation.png', dpi=500)
