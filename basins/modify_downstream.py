import gsflow 
import numpy as np

region = 8
region_name = '20210730_v11_gm_r' + str(region).zfill(2)
print('processing region ' + region_name)
orig_model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/regions/' + region_name
new_model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/basins/' + region_name
control_file = orig_model_dir+'/control.default.bandit'
gs = gsflow.GsflowModel.load_from_file(control_file=control_file)
ctl = gs.control 
par = gs.prms.parameters
mod_par = gsflow.prms.PrmsParameters(parameters_list=[])

segment_index = 121
obs_index = 157
mod_filename = 'mod_downstream.param'
for params in par.record_names:
    par_orig = par.get_record(params)
    if par_orig.name == 'nobs':
        mod_par.add_record(name=par_orig.name, values=[obs_index], dimensions=par_orig._dimensions, file_name=new_model_dir + '/' + mod_filename)
    elif par_orig.name == 'obsin_segment':
        orig_values = par_orig._values
        orig_values[segment_index - 1] = obs_index
        mod_par.add_record(name=par_orig.name, values=par_orig._values, dimensions=par_orig._dimensions, file_name=new_model_dir + '/' + mod_filename)
    else:
        mod_par.add_record(name=par_orig.name, values=par_orig._values, dimensions=par_orig._dimensions, file_name=new_model_dir + '/' + mod_filename)
for ctl_param in ctl.record_names:
    par_orig = ctl.get_record(ctl_param)
    if 'file' in par_orig.name and isinstance(par_orig._values[0], str):
        orig_path = par_orig._values[0].split('/')
        ctl.set_values(name=par_orig.name, values=[new_model_dir + '/' + orig_path[-1]])
ctl.set_values(name='data_file', values=[new_model_dir + '/new_sf_data'])
ctl.set_values(name='param_file', values=[mod_filename])
ctl.write(name=new_model_dir+'/control.default.bandit')
mod_par.write()


region = 15
region_name = '20210730_v11_gm_r' + str(region).zfill(2)
print('processing region ' + region_name)
orig_model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/regions/' + region_name
new_model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/basins/' + region_name
control_file = orig_model_dir+'/control.default.bandit'
gs = gsflow.GsflowModel.load_from_file(control_file=control_file)
ctl = gs.control
par = gs.prms.parameters
mod_par = gsflow.prms.PrmsParameters(parameters_list=[])

segment_index = 1192
obs_index = 183
mod_filename = 'mod_downstream.param'
for params in par.record_names:
    par_orig = par.get_record(params)
    if par_orig.name == 'nobs':
        mod_par.add_record(name=par_orig.name, values=[obs_index], dimensions=par_orig._dimensions, file_name=new_model_dir + '/' + mod_filename)
    elif par_orig.name == 'obsin_segment':
        orig_values = par_orig._values
        orig_values[segment_index - 1] = obs_index
        mod_par.add_record(name=par_orig.name, values=par_orig._values, dimensions=par_orig._dimensions, file_name=new_model_dir + '/' + mod_filename)
    else:
        mod_par.add_record(name=par_orig.name, values=par_orig._values, dimensions=par_orig._dimensions, file_name=new_model_dir + '/' + mod_filename)
for ctl_param in ctl.record_names:
    par_orig = ctl.get_record(ctl_param)
    if 'file' in par_orig.name and isinstance(par_orig._values[0], str):
        orig_path = par_orig._values[0].split('/')
        ctl.set_values(name=par_orig.name, values=[new_model_dir + '/' + orig_path[-1]])
ctl.set_values(name='data_file', values=[new_model_dir + '/new_sf_data'])
ctl.set_values(name='param_file', values=[mod_filename])
ctl.write(name=new_model_dir+'/control.default.bandit')
mod_par.write()

