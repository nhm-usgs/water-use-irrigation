import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import calendar
import os 
out_dir =  '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/test_model/prms/projects/yampa/output/'
hru_list = [85535, 85637, 85620, 85414]  # nhru_v11 (not nhm_id)
hru_name = ['Steamboat', 'Craig', 'Hayden', 'Yampa']

# get key to convert nhm_id to model_idx:
idx_key = pd.read_csv('yampa_idx_to_nhru.csv', header=0)
# Irrigated Area (acres):
hru_areas = pd.read_csv('hru_area.csv', header=0)
ag_fracs = pd.read_csv('yampa_ia15.csv', header=0)

dt_format = '%Y-%m-%d'
# applied irrigation (from NHM/PRMS)
irr = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_irrigation_add.csv'))
irr.columns = [str(c) for c in range(len(irr.columns))]
irr_date_list = np.array([datetime.datetime.strptime(irr['0'].iloc[i], dt_format) for i, dummy in irr.iterrows()])

# applied irrigation (from NHM/PRMS)
irr_vol = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_irrigation_add_vol.csv'))
irr_vol.columns = [str(c) for c in range(len(irr_vol.columns))]
irr_vol_date_list = np.array([datetime.datetime.strptime(irr_vol['0'].iloc[i], dt_format) for i, dummy in irr_vol.iterrows()])

# actual ET (from NHM/PRMS)
actet = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_actet.csv'))
actet.columns = [str(c) for c in range(len(actet.columns))]
actet_date_list = np.array([datetime.datetime.strptime(actet['0'].iloc[i], dt_format) for i, dummy in actet.iterrows()])

# potential ET (from NHM/PRMS)
#potet = pd.read_csv(os.path.join(out_dir, 'nhru_summary_potet.csv'))
#potet.columns = [str(c) for c in range(len(actet.columns))]
#potet_date_list = np.array([datetime.datetime.strptime(potet['0'].iloc[i], dt_format) for i, dummy in potet.iterrows()])

# runoff (from NHM/PRMS)
runoff = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_hortonian.csv'))
runoff.columns = [str(c) for c in range(len(runoff.columns))]
runoff_date_list = np.array([datetime.datetime.strptime(runoff['0'].iloc[i], dt_format) for i, dummy in runoff.iterrows()])

# percolation (from NHM/PRMS)
perc = pd.read_csv(os.path.join(out_dir, 'nhru_summary_ag_soil2gvr.csv'))
perc.columns = [str(c) for c in range(len(perc.columns))]
perc_date_list = np.array([datetime.datetime.strptime(perc['0'].iloc[i], dt_format) for i, dummy in perc.iterrows()])

start_date = datetime.datetime(1980, 10, 1)
end_date = datetime.datetime(1988, 9, 30)
# start_date = datetime.datetime(2016, 1, 1)
# end_date = datetime.datetime(2016, 9, 30)
days = (end_date - start_date).days + 1
plot_date_list = [start_date + datetime.timedelta(days=d) for d in range(days)]

# OpenET from output files
#et2 = pd.read_csv(os.path.join(out_dir, 'nhru_summary_AET_external.csv'))
#et2.columns = [str(c) for c in range(len(et2.columns))]
#et2_date_list = np.array([datetime.datetime.strptime(et2['0'].iloc[i], dt_format) for i, dummy in et2.iterrows()])

#eto2 = pd.read_csv(os.path.join(out_dir, 'nhru_summary_PET_external.csv'))
#eto2.columns = [str(c) for c in range(len(eto2.columns))]
#eto2_date_list = np.array([datetime.datetime.strptime(eto2['0'].iloc[i], dt_format) for i, dummy in eto2.iterrows()])

fig, axes = plt.subplots(2, 2, figsize=(13.33, 7.5))
axes = axes.flat
fig1, axes1 = plt.subplots(2, 2, figsize=(13.33, 7.5))
axes1 = axes1.flat
for num, hru in enumerate(hru_name):
    idx_from_hru = str(idx_key['model_idx'][idx_key['nhru_v11'] == hru_list[num]].item())
    hru_area = hru_areas['hru_area'][int(idx_from_hru)-1]
    ag_frac = ag_fracs['MEAN'][int(idx_from_hru)-1]
    irr_area = hru_area * ag_frac
    irr_data = irr[idx_from_hru][(start_date <= irr_date_list) & (irr_date_list <= end_date)]
    irr_vol_data = irr_vol[idx_from_hru][(start_date <= irr_vol_date_list) & (irr_vol_date_list <= end_date)]
    actet_data = actet[idx_from_hru][(start_date <= actet_date_list) & (actet_date_list <= end_date)]
    #potet_data = potet[idx_from_hru][(start_date <= potet_date_list) & (potet_date_list <= end_date)]
    runoff_data = runoff[idx_from_hru][(start_date <= runoff_date_list) & (runoff_date_list <= end_date)]
    perc_data = perc[idx_from_hru][(start_date <= perc_date_list) & (perc_date_list <= end_date)]
    #et2_data = et2[idx_from_hru][(start_date <= et2_date_list) & (et2_date_list <= end_date)]
    #eto2_data = eto2[idx_from_hru][(start_date <= eto2_date_list) & (eto2_date_list <= end_date)]
    #axes[num].plot(plot_date_list, et2_data, label='ETa (OpenET)')
    #axes[num].plot(plot_date_list, eto2_data, label='ETo (OpenET)')
    axes[num].plot(plot_date_list, actet_data, label='ETa (NHM/PRMS')
    #axes[num].plot(plot_date_list, potet_data, label='ETo (NHM/PRMS)')
    axes1[num].plot(plot_date_list, irr_data, label='Applied Irrigation\n(model output in inches)', color='tab:purple')
    axes1[num].plot(plot_date_list, irr_vol_data / irr_area, label='Applied Irrigation\n(model output in acre inches\ndivided by irrigated area)', color='tab:pink')
    axes1[num].plot(plot_date_list, runoff_data, label='Runoff', color='tab:cyan')
    axes1[num].plot(plot_date_list, perc_data, label='Percolation', color='tab:brown')
    if num == 0:
        handles, labels = axes[num].get_legend_handles_labels()
    axes_dates = [' ' + calendar.month_name[i+1][0:3] for i in range(9)]
    axes[num].set_xticks(axes[num].get_xticks()[0:9])
    axes[num].set_xticklabels(axes_dates, rotation=45, ha='left')
    axes[num].set_title(hru + '\nIrrigated Fraction: ' + str(np.round(ag_frac, 2)))
    if (num == 0) or (num == 3):
        axes[num].set_ylabel('Inches\nper\nDay', ha='right', va='center', ma='left', rotation=0)
    axes[num].set_ylim([0, 0.26])
    if num == 0:
        handles1, labels1 = axes1[num].get_legend_handles_labels()
    axes1[num].set_xticks(axes1[num].get_xticks()[0:9])
    axes1[num].set_xticklabels(axes_dates, rotation=45, ha='left')
    axes1[num].set_title(hru + '\nIrrigated Fraction: ' + str(np.round(ag_frac, 2)))
    if (num == 0) or (num == 3):
        axes1[num].set_ylabel('Inches\nper\nDay', ha='right', va='center', ma='left', rotation=0)
    # axes[num].set_ylim([0, 100])
fig.legend(handles, labels)
fig.tight_layout()
fig.suptitle('2016 ET:\nUpper Colorado River Basin', fontsize=20)
fig.subplots_adjust(top=0.8)
fig.savefig('ET.png', dpi=500)

fig1.legend(handles1, labels1)
fig1.tight_layout()
fig1.suptitle('2016 Applied Irrigation, Runoff, and Percolation:\nUpper Colorado River Basin', fontsize=20)
fig1.subplots_adjust(top=0.75)
fig1.savefig('irr_runoff_perc.png', dpi=500)

