import gsflow 
import numpy as np


model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/test_model/prms/projects/ucb/'
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
ctl_str = [item.name for item in ctl.records_list]
for ctl_vars in ctl_str:
    if ctl_vars not in ex_str:
        ctl.remove_record(name=ctl_vars)
print('adding new control parameters...')
ctl_str = [item.name for item in ctl.records_list]
for ex_vars in ex_ctl.records_list:
    if ex_vars.name not in ctl_str:
        ctl.add_record(name=ex_vars.name, values=ex_vars.values) 
    ctl.set_values(name=ex_vars.name, values=ex_vars.values)
#activate ag
new_record_list = [
        ('dyn_ag_frac_flag', 1), 
        ('ag_frac_dynamic', './input/dyn_ag_frac.param'),
        ('AET_cbh_file', './input/actet_openet.cbh'),
        ('PET_cbh_file', './input/potet_openet.cbh')]
print('adding ag control parameters...')
ctl_str = [item.name for item in ctl.records_list]
for rec in new_record_list: 
    rec_name = rec[0]
    if rec_name in ctl_str: 
        ctl.set_values(name=rec[0], values=[rec[1]])
    else: 
        ctl.add_record(name=rec[0], values=[rec[1]])
print('adding other miscellaneous items...')
ctl.set_values(name='nhruOutVar_Names', values=['unused_potet', 'ag_irrigation_add', 'hru_actet', 'potet', 'AET_external', 'PET_external'])
ctl.set_values(name='data_file', values=['./input/sf_data'])
ctl.set_values(name='model_output_file', values=['./output/model.out'])
ctl.set_values(name='var_init_file', values=['./prms_ic.in'])
ctl.set_values(name='var_save_file', values=['./output/prms_ic.out'])
ctl.set_values(name='csv_output_file', values=['./output/prms_summary.csv'])
ctl.set_values(name='stat_var_file', values=['./output/statvar.out'])
ctl.set_values(name='ani_output_file', values=['./animation.out'])

base_filename = './input/ucb.param'
for params in par.record_names:
    new_record = par.get_record(params)
    new_record.file_name = model_dir+base_filename

# parameters, which are not dynamic 
ag_list = ['ag_soil_moist_max', 'ag_soil_moist_init_frac', 'ag_soil_rechr_max_frac', 'ag_soil_rechr_init_frac', 'sro_to_dprst_ag', 'pref_flow_infil_frac']
orig_list = ['soil_moist_max', 'soil_moist_init_frac', 'soil_rechr_max_frac', 'soil_rechr_init_frac', 'sro_to_dprst_perv', 'pref_flow_den']
ag_filename = './input/ag.ucb.param'
for ind, ag_var in enumerate(ag_list): 
    if ag_var not in par.record_names:
        par_orig = par.get_record(orig_list[ind])
        ag_par.add_record(name=ag_var, values=par_orig._values, dimensions=par_orig._dimensions, file_name=model_dir+ag_filename)
ag_par.add_record(name='ppt_zero_thresh', values=[0.0], dimensions=[['one', 1]], datatype=2, file_name=model_dir+ag_filename)
ag_par.add_record(name='max_soilzone_ag_iter', values=[500], dimensions=[['one', 1]], datatype=1, file_name=model_dir+ag_filename)
ag_par.add_record(name='soilzone_aet_converge', values=[0.005], dimensions=[['one', 1]], datatype=2, file_name=model_dir+ag_filename)


par_control_rec = ctl.get_record(name='param_file')
ctl.set_values(name='param_file', values=[base_filename, ag_filename]) 
par.write()
ag_par.write()
ctl.write(name=model_dir+'ucb.control')
