import os
import pandas as pd
import datetime
import numpy as np
import calendar
import pickle


def save_pickles(dict_, filename_):
    with open(os.path.join(filename_+'.pickle'), 'wb') as handle:
        pickle.dump(dict_, handle)
    return


def open_pickles(filename_):
    with open(os.path.join(filename_+'.pickle'), 'rb') as handle:
        df_ = pickle.load(handle)
    return df_


def fortranformat(n):
    a = '{:.3E}'.format(float(n))
    e = a.find('E')
    return '0.{}{}{}{:02d}'.format(a[0],a[2:e],a[e:e+2],abs(int(a[e+1:])*1+1))


def build_idx_dicts():
    idx_key = pd.read_csv('idx_to_nhru.csv', header=0)
    nhmid_dict_ = {}
    idx_dict_ = {}
    nhmid_list_ = []
    for ind, line in idx_key.iterrows():
        idx_dict_[line['nhm_id']] = line['model_idx']
        nhmid_dict_[line['model_idx']] = line['nhm_id']
        nhmid_list_.append(line['nhm_id'])
    idx_col_ = idx_key['model_idx'].tolist()
    return idx_dict_, nhmid_dict_, idx_col_, nhmid_list_


def build_dataframe():
    df = False
    for filename in os.listdir('openet_daily'):
        if filename.endswith('.csv'):
            print('processing ' + filename + '...')
            data = pd.read_csv(os.path.join('openet_daily', filename), header=0, dtype={'date_mean':int, 'nhm_id':int, 'et_mean':float, 'et_reference_mean':float})
            if not df:
                file_df = data
                df = True
            else:
                file_df = pd.concat([file_df, data])
    file_df = file_df[~np.isnan(file_df.et_reference_mean) & ~np.isnan(file_df.et_mean)]
    file_df = file_df[file_df['nhm_id'].isin(nhmid_list)]
    file_df = file_df[file_df['date_mean'] <= 20160930.0]
    file_df.sort_values(by='date_mean')
    idx_column = []
    for ind, line in file_df.iterrows():
        idx_column.append(idx_dict[int(line['nhm_id'])])
    file_df.insert(0, 'IDX', idx_column)
    return file_df


def write_datafile():
    first_time = False
    if first_time:
        all_data = build_dataframe()
        save_pickles(all_data, 'all_data')
    else:
        all_data = open_pickles('all_data')
    start_date = datetime.date(1980, 10, 1)
    end_date = datetime.date(2016, 9, 30)
    days = (end_date-start_date).days + 1
    date_list = [start_date + datetime.timedelta(days=d) for d in range(days)]
    new_index = [int(str(day.year) + str(day.month).zfill(2) + str(day.day).zfill(2)) for day in date_list]
    potet_df = pd.read_csv('potet.day', header=None, delim_whitespace=True)
    actet_df = pd.read_csv('actet.day', header=None, delim_whitespace=True)
    potet_df.drop(potet_df.columns[[0, 1, 2, 3, 4, 5]], axis=1, inplace=True)
    actet_df.drop(actet_df.columns[[0, 1, 2, 3, 4, 5]], axis=1, inplace=True)
    potet_df.columns = idx_col
    actet_df.columns = idx_col
    potet_df.insert(0, 'Date_Int', new_index)
    actet_df.insert(0, 'Date_Int', new_index)
    potet_df.set_index('Date_Int', inplace=True, drop=False)
    actet_df.set_index('Date_Int', inplace=True, drop=False)
    # potet_df.loc[all_data['date_mean'], all_data['IDX']] = all_data['et_reference_mean'] * 0.0393701
    # actet_df.loc[all_data['date_mean'], all_data['IDX']] = all_data['et_mean'] * 0.0393701
    for ind, line in all_data.iterrows():
        potet_df.loc[int(line['date_mean']), int(line['IDX'])] = line['et_reference_mean'] * 0.0393701
        actet_df.loc[int(line['date_mean']), int(line['IDX'])] = line['et_mean'] * 0.0393701
    # files
    eto = open('potet_openet.cbh', 'w')
    eto.write('OpenET ETo passed to NHM-PRMS as PET\n')
    eto.write('potet    3851\n')
    eto.write('########################################\n')
    for ind, line in potet_df.iterrows():
        dateint = str(int(line['Date_Int']))
        eto.write(str(dateint[0:4]) + ' ' + str(int(dateint[4:6])).rjust(2) + ' ' + str(int(dateint[-2:])).rjust(2) + ' 0 0 0  ')
        for ind, item in enumerate(line):
            if ind > 0:
                eto.write(fortranformat(item) + '  ')
        eto.write('\n')
    eto.close()
    et = open('actet_openet.cbh', 'w')
    et.write('OpenET ETa passed to NHM-PRMS as AET\n')
    et.write('actet    3851\n')
    et.write('########################################\n')
    for ind, line in actet_df.iterrows():
        dateint = str(int(line['Date_Int']))
        et.write(str(dateint[0:4]) + ' ' + str(int(dateint[4:6])).rjust(2) + ' ' + str(int(dateint[-2:])).rjust(2) + ' 0 0 0  ')
        for ind, item in enumerate(line):
            if ind > 0:
                et.write(fortranformat(item) + '  ')
        et.write('\n')
    et.close()


idx_dict, nhmid_dict, idx_col, nhmid_list = build_idx_dicts()
write_datafile()
