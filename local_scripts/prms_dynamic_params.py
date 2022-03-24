import os,sys
import datetime


class Dparam(object):
    def __init__(self, name, file_name, data):
        self.name = name
        self.file_name = file_name
        self.data = data

    def to_file(self):
        fidw = open(self.file_name, 'w')
        header = self.data['header']
        for h in header:
            fidw.write(h)
            fidw.write('\n')
        # order dates
        dates = []
        for key in self.data.keys():
            if 'header' in key:
                continue
            dates.append(datetime.date(year=key[0], month=key[1], day= key[2]))
        dates.sort()
        str_val = []
        for dt in dates:
            date_tuple = (dt.year, dt.month, dt.day)
            curr_data = self.data[date_tuple]
            str_val.append('{} {} {}\n'.format(dt.year, dt.month, dt.day))

            for val in curr_data:
                str_val.append('{}\n'.format(val))
        str_val = ''.join(str_val)
        str_val = str_val[:-1]
        fidw.write(str_val)

        fidw.close()


class Dyn_param(object):
    def __init__(self, gs):
        self.gs = gs
        self._get_dyn_info()

    def _get_dyn_info(self):
        self.dyn_params = []
        self.dyn_files = {}
        for rec in self.gs.prms.control.record_names:
            if "_dynamic" in rec:
                self.dyn_params.append(rec)
                self.dyn_files[rec] = self.gs.prms.control.get_record(rec).values[0]



    def get_dyn_param(self, parname):

        model_dir, name = os.path.split(self.gs.control_file)
        parfile = os.path.join(model_dir, self.dyn_files[parname])
        par_data = self._read_dyn_file(parfile)
        Dparm = Dparam(name = parname, file_name=parfile, data=par_data)
        return Dparm


    def _read_dyn_file(self, fname):
        fidr = open(fname, 'r')
        content = fidr.readlines()
        fidr.close()
        par_data = {}
        flg_header = True
        par_data['header'] = []
        for i, line in enumerate(content):
            if flg_header:
                par_data['header'].append(line.strip())
                if '###' in line:
                    flg_header = False
                continue
            # read data that is not header
            parts = line.strip().split()
            if len(parts) == 3:
                # this is date
                curr_date = (int(parts[0]), int(parts[1]), int(parts[2]))
                par_data[curr_date] = []
                continue
            else:
                par_data[curr_date].append(float(line.strip()))

        return par_data



