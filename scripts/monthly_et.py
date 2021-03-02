import os
import pandas as pd
import datetime
import numpy as np
import calendar


def fortranformat(n):  # thank you stack exchange
    a = '{:.3E}'.format(float(n))
    e = a.find('E')
    return '0.{}{}{}{:02d}'.format(a[0],a[2:e],a[e:e+2],abs(int(a[e+1:])*1+1))


def build_file_dictionary():
    file_dict_ = {}
    for yr in range(2016, 2020):
        eto = pd.read_csv('/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/USGS_HRU_LANDID_2016-2019/USGS_' + str(yr) + '_ensemble_eto.csv', header=0)
        et = pd.read_csv('/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/USGS_HRU_LANDID_2016-2019/USGS_' + str(yr) + '_ensemble_et.csv', header=0)
        dt_format = '%Y-%m-%d'
        eto_date_list = np.array([datetime.datetime.strptime(eto['time'].iloc[i], dt_format) for i, dummy in eto.iterrows()])
        eto.set_index(eto_date_list, inplace=True)
        et_date_list = np.array([datetime.datetime.strptime(et['time'].iloc[j], dt_format) for j, dummy in et.iterrows()])
        et.set_index(et_date_list, inplace=True)
        file_dict_[yr] = (eto, et)
    return file_dict_


def write_datafile():
    ucb_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/test_model/prms/projects/ucb/input/'
    # potet file for pre-2016:
    infile = open(ucb_dir+'potet.day', 'r')
    # get key to convert nhm_id to model_idx:
    idx_key = pd.read_csv('idx_to_nhru.csv', header=0)
    idx_key.set_index('model_idx', drop=False, inplace=True)
    # files
    eto = open(ucb_dir+'potet_openet.cbh', 'w')
    et = open(ucb_dir+'actet_openet.cbh', 'w')
    # first line
    eto.write('OpenET ETO passed to NHM-PRMS as PET\n')
    et.write('OpenET ET passed to NHM-PRMS as AET\n')
    # second line
    eto.write('potet    3851\n')
    et.write('actet    3851\n')
    # third line
    eto.write('########################################\n')
    et.write('########################################\n')
    start_date = datetime.date(2016, 1, 1)
    end_date = datetime.date(2016, 9, 30)
    days = (end_date-start_date).days + 1
    date_list = [start_date + datetime.timedelta(days=d) for d in range(days)]
    for row, line in enumerate(infile):
        if (row > 2) and (row < 12878):
            split_lines = line.split()
            et.write(line[0:18])
            for col, item in enumerate(split_lines):
                if col > 5:
                    fl = float(item) * 0.9
                    fl_fort = fortranformat(fl)
                    et.write(fl_fort + '  ')
            eto.write(line)
            et.write('\n')
    infile_lines = open(ucb_dir+'potet.day', 'r').readlines()
    for day in date_list:  # loop through days of simulation
        dummy, days_in_month = calendar.monthrange(day.year, day.month)
        eto.write(str(day.year) + ' ' + str(day.month).rjust(2) + ' ' + str(day.day).rjust(2) + ' 0 0 0  ')
        et.write(str(day.year) + ' ' + str(day.month).rjust(2) + ' ' + str(day.day).rjust(2) + ' 0 0 0  ')
        if day.day == 1:
            eto_array = np.zeros(len(idx_key['model_idx']))
            et_array = np.zeros(len(idx_key['model_idx']))
            data_date = datetime.datetime(day.year, day.month, 1)
            # get files:
            eto_file = file_dict[day.year][0]
            et_file = file_dict[day.year][1]
            for idx in range(len(idx_key['model_idx'])):  # loop through HRUs
                nhru = idx_key['nhru_v11'][idx + 1]
                data_line = 12878 + (day.day - start_date.day)
                fill_vals = infile_lines[data_line].split()
                # pull corresponding data and write it:
                if nhru in eto_file['nhm_id'].tolist():
                    eto_subset = (eto_file['nhm_id'] == nhru) & (eto_file.index == data_date)
                    eto_idx = np.mean(eto_file['mean'][eto_subset]) / days_in_month
                    eto_array[idx] = eto_idx
                else:
                    eto_array[idx] = float(fill_vals[6+idx])
                if nhru in et_file['nhm_id'].tolist():
                    et_subset = (et_file['nhm_id'] == nhru) & (et_file.index == data_date)
                    et_idx = np.mean(et_file['mean'][et_subset]) / days_in_month
                    et_array[idx] = et_idx
                else:
                    et_array[idx] = 0.9*float(fill_vals[6+idx])
                eto.write(fortranformat(eto_array[idx]) + '  ')
                et.write(fortranformat(et_array[idx]) + '  ')
            eto.write('\n')
            et.write('\n')
        else:
            for idx in range(len(idx_key['model_idx'])):  # loop through HRUs
                eto.write(fortranformat(eto_array[idx]) + '  ')
                et.write(fortranformat(et_array[idx]) + '  ')
            eto.write('\n')
            et.write('\n')
    eto.close()
    et.close()


file_dict = build_file_dictionary()
write_datafile()

