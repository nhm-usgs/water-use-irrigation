import gsflow 
import numpy as np

model_dir = '../yampa/'
control_file = model_dir+'control.default.bandit'
gs = gsflow.GsflowModel.load_from_file(control_file=control_file)
ctl = gs.control 
par = gs.prms.parameters
ag_par = gsflow.prms.PrmsParameters(parameters_list=[]) 

example_control_file = '../../test_model/prms/projects/yampa/yampa.control'
ex_gs = gsflow.GsflowModel.load_from_file(control_file=example_control_file)
ex_ctl = ex_gs.control 

print('removing extra control parameters...')
ex_str = [item.name for item in ex_ctl.records_list]
for ctl_vars in ctl.records_list:
    if ctl_vars.name not in ex_str: 
        ctl.remove_record(name=ctl_vars.name)
print('adding new control parameters...')
ctl_str = [item.name for item in ctl.records_list]
for ex_vars in ex_ctl.records_list:
    if ex_vars.name not in ctl_str:
        ctl.add_record(name=ex_vars.name, values=ex_vars.values) 

#activate ag
new_record_list = [('agriculture_soil_flag', 1), 
        ('model_mode', 'PRMS_AG'),
        ('executable_model', '../../bin/gsflow.exe'), 
        ('dyn_ag_frac_flag', 1), 
        ('ag_frac_dynamic', './input/dyn_ag_frac.param'),
        ('data_file', './input/sf_data'), 
        ('model_output_file', './output/model.out'),
        ('var_save_file', './output/prms_ic.out'),
        ('csv_output_file', './output/prms_summary'),
        ('nhruOutBaseFileName', './output/nhru_summary_'),
        ('stat_var_file', './output/statvar.out'),
        ('dprst_transfer_file', './input/dprst.transfer'),
        ('ext_transfer_file', './input/ext.transfer'),
        ('gwr_transfer_file', './input/gwr.transfer'),
        ('segment_transfer_file', './input/seg.transfer'),
        ('nsegmentOutBaseFileName', './output/nsegment_summary_'),
        ('precip_day', './input/prcp.cbh'),
        ('tmax_day', './input/tmax.cbh'),
        ('tmin_day', './input/tmin.cbh'),
        ('PET_cbh_file', './input/potet.day'),
        ('AET_cbh_file', './input/actet.day'), 
        ('AET_module', 'climate_hru'),
        ('PET_ag_module', 'climate_hru')]
ctl.set_values(name='PET_cbh_file', values=['./input/potet.day'])
ctl.set_values(name='AET_cbh_file', values=['./input/actet.day'])

print('adding ag control parameters...')
ctl_str = [item.name for item in ctl.records_list]
for rec in new_record_list: 
    rec_name = rec[0]
    if rec_name in ctl_str: 
        ctl.set_values(name=rec[0], values=[rec[1]])
    else: 
        ctl.add_record(name=rec[0], values=[rec[1]])
ctl.set_values(name='nhruOutVar_Names', values=['unused_potet', 'ag_irrigation_add', 'hru_actet', 'potet'])

base_filename = './input/yampa.param'
for params in par.record_names:
    new_record = par.get_record(params)
    new_record.file_name = model_dir+base_filename

# parameters, which are not dynamic 
ag_list = ['ag_soil_moist_max', 'ag_soil_moist_init_frac', 'ag_soil_rechr_max_frac', 'ag_soil_rechr_init_frac', 'sro_to_dprst_ag']
orig_list = ['soil_moist_max', 'soil_moist_init_frac', 'soil_rechr_max_frac', 'soil_rechr_init_frac', 'sro_to_dprst_perv']
ag_filename = './input/ag.yampa.param'
for ind, ag_var in enumerate(ag_list): 
    if ag_var not in par.record_names:
        par_orig = par.get_record(orig_list[ind])
        ag_par.add_record(name=ag_var, values=par_orig._values, dimensions=par_orig._dimensions, file_name=model_dir+ag_filename)

par_control_rec = ctl.get_record(name='param_file')
ctl.set_values(name='param_file', values=[base_filename, ag_filename]) 
par.write()
ag_par.write()
ctl.write(name=model_dir+'yampa.control')

