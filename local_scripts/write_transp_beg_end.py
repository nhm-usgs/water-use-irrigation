import pandas as pd
import datetime
import numpy as np
import os


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


def mon_from_doy(doy):  # I'm sure calendar or datetime does this but this didn't take too long
    if 0 < doy <= 31:
        mon = 1
    elif 31 < doy <= (31 + 28):
        mon = 2
    elif (31 + 28) < doy <= (31 + 28 + 31):
        mon = 3
    elif (31 + 28 + 31) < doy <= (31 + 28 + 31 + 30):
        mon = 4
    elif (31 + 28 + 31 + 30) < doy <= (31 + 28 + 31 + 30 + 31):
        mon = 5
    elif (31 + 28 + 31 + 30 + 31) < doy <= (31 + 28 + 31 + 30 + 31 + 30):
        mon = 6
    elif (31 + 28 + 31 + 30 + 31 + 30) < doy <= (31 + 28 + 31 + 30 + 31 + 30 + 31):
        mon = 7
    elif (31 + 28 + 31 + 30 + 31 + 30 + 31) < doy <= (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31):
        mon = 8
    elif (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31) < doy <= (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30):
        mon = 9
    elif (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30) < doy <= (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31):
        mon = 10
    elif (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31) < doy <= (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30):
        mon = 11
    elif (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30) < doy <= (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31):
        mon = 12
    return mon


idx_dict, nhmid_dict, idx_col, nhmid_list = build_idx_dicts()
transp_beg_arr = np.zeros(3851)
transp_end_arr = np.zeros(3851)
irrigation_season = pd.read_csv(os.path.join('UCRB', 'MyProject', 'irrigation_season.csv'))
for ind, line in irrigation_season.iterrows():
    idx = idx_dict[line['nhm_id']] - 1
    days = line.iloc[2:].to_numpy()
    transp_beg = mon_from_doy(np.argmin(np.abs(days - 1)) + 1)
    transp_end = mon_from_doy(len(days) - np.argmin(np.flip(np.abs(days - 1))))
    transp_beg_arr[idx] = transp_beg
    transp_end_arr[idx] = transp_end
np.savetxt('transp_beg.txt', transp_beg_arr, fmt='%.1i')
np.savetxt('transp_end.txt', transp_end_arr, fmt='%.1i')
