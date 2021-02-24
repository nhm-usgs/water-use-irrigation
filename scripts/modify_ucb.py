import gsflow 
import numpy as np


model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/test_model/prms/projects/ucb/'
control_file = model_dir+'control.default.bandit'
gs = gsflow.GsflowModel.load_from_file(control_file=control_file)
ctl = gs.control 
par = gs.prms.parameters
ag_par = gsflow.prms.PrmsParameters(parameters_list=[]) 

example_control_file = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/test_model/prms/projects/ucb/ucb.control'
ex_gs = gsflow.GsflowModel.load_from_file(control_file=example_control_file)
ex_ctl = ex_gs.control 

for ctl_vars in ctl.records_list:
    if ctl_vars not in ex_ctl.records_list: 
        ctl.remove_record(name=ctl_vars.name)
for ex_vars in ex_ctl.records_list:
    if ex_vars not in ctl.records_list: 
        ctl.add_record(name=ex_vars.name, values=ex_vars.values) 

#activate ag
ctl.add_record(name='agriculture_soil_flag', values=[1])
ctl.set_values(name='model_mode', values=['PRMS_AG'])
ctl.set_values(name='executable_model', values=['../../bin/gsflow.exe'])
ctl.add_record(name='dyn_ag_frac_flag', values=[1])
ctl.add_record(name='ag_frac_dynamic', values=['./input/dyn_ag_frac.param'])
# change to Steve's IO structure 
ctl.set_values(name='data_file', values=['./input/sf_data'])
ctl.set_values(name='model_output_file', values=['./output/model.out'])
ctl.set_values(name='var_save_file', values=['./output/prms_ic.out'])
ctl.set_values(name='csv_output_file', values=['./output/prms_summary'])
ctl.set_values(name='nhruOutBaseFileName', values=['./output/nhru_summary_'])
ctl.set_values(name='stat_var_file', values=['./output/statvar.out'])
ctl.set_values(name='dprst_transfer_file', values=['./input/dprst.transfer'])
ctl.set_values(name='ext_transfer_file', values=['./input/ext.transfer'])
ctl.set_values(name='gwr_transfer_file', values=['./input/gwr.transfer'])
ctl.set_values(name='segment_transfer_file', values=['./input/seg.transfer'])
ctl.set_values(name='nsegmentOutBaseFileName', values=['./output/nsegment_summary_'])
ctl.set_values(name='tmin_day', values=['./input/tmin.cbh'])
# other small changes: 
ctl.set_values(name='nhruOutVar_Names', values=['unused_potet', 'ag_irrigation_add', 'hru_actet', 'potet'])


base_filename = './input/ucb.param'
for params in par.record_names:
    new_record = par.get_record(params)
    new_record.file_name = model_dir+base_filename

# parameters, which are not dynamic 
ag_list = ['ag_soil_moist_max', 'ag_soil_moist_init_frac', 'ag_soil_rechr_max_frac', 'ag_soil_rechr_init_frac', 'sro_to_dprst_ag']
orig_list = ['soil_moist_max', 'soil_moist_init_frac', 'soil_rechr_max_frac', 'soil_rechr_init_frac', 'sro_to_dprst_perv']
ag_filename = './input/ag.ucb.param'
for ind, ag_var in enumerate(ag_list): 
    if ag_var not in par.record_names:
        par_orig = par.get_record(orig_list[ind])
        ag_par.add_record(name=ag_var, values=par_orig._values, dimensions=par_orig._dimensions, file_name=model_dir+ag_filename)

par_control_rec = ctl.get_record(name='param_file')
ctl.set_values(name='param_file', values=[base_filename, ag_filename]) 
par.write()
ag_par.write()
ctl.write(name=model_dir+'ucb.control')

