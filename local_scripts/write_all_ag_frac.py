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


def write_dynamic_param(filename):
    start_date = datetime.date(1980, 10, 1)
    end_date = datetime.date(2016, 9, 30)
    outfile = open(filename, 'w')
    idx_str = [str(x) for x in idx_col]
    outfile.write('year month day HRU ' + " ".join(idx_str))
    outfile.write('\n####')
    time_list = pd.date_range(start_date, end_date)
    for ind, time in enumerate(time_list):
        if (time.day == 1) and (time.month == 1):
            if time.year < 1997:
                infile = pd.read_csv(os.path.join('UCRB', 'MyProject', 'lanid_1997.csv'))
            else:
                infile = pd.read_csv(os.path.join('UCRB', 'MyProject', 'lanid_' + str(time.year) + '.csv'))
            outfile.write('\n')
            outfile.write(str(time.year) + ' ' + str(time.month) + ' ' + str(time.day) + ' ')
            values = infile['MEAN']
            outfile.write(" ".join(np.round(values, 2).astype(str).tolist()))
    outfile.close()


def write_initial_ag_frac(filename):
    infile = pd.read_csv(os.path.join('UCRB', 'MyProject', 'lanid_1997.csv'))
    values = infile['MEAN']
    outfile = open(filename, 'w')
    outfile.write("\n".join(np.round(values, 2).astype(str).tolist()))
    outfile.close()


idx_dict, nhmid_dict, idx_col, nhmid_list = build_idx_dicts()
write_dynamic_param('dyn_ag_frac.param', )
write_initial_ag_frac('initial_ag_frac.txt')