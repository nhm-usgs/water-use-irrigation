import gsflow 
import numpy as np


model_dir = '../yampa/'
control_file = model_dir+'control.default.bandit'
gs = gsflow.GsflowModel.load_from_file(control_file=control_file)
ctl = gs.control 
par = gs.prms.parameters
ag_par = gsflow.prms.PrmsParameters(parameters_list=[]) 

# ag_frac, which is dynamic 
ctl.add_record(name='dyn_ag_frac_flag', values=[1])
ctl.add_record(name='ag_frac_dynamic', values=['dyn_ag_frac.param'])


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

