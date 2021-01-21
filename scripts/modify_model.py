from gsflow import GsflowModel
import numpy as np

control_file = r"../yampa/control.default.bandit"
gs = GsflowModel.load_from_file(control_file=control_file)
ctl = gs.control 
par = gs.prms.parameters

# ag_frac, which is dynamic 
ctl.add_record(name='dyn_ag_frac_flag', values=[1])
ctl.add_record(name='ag_frac_dynamic', values=['dyn_ag_frac.param'])

# parameters, which are not dynamic 
ag_list = ['ag_soil_moist_max', 'ag_soil_moist_init_frac', 'ag_soil_rechr_max_frac', 'ag_soil_rechr_init_frac', 'sro_to_dprst_ag']
orig_list = ['soil_moist_max', 'soil_moist_init_frac', 'soil_rechr_max_frac', 'soil_rechr_init_frac', 'sro_to_dprst_perv']
for ind, ag_var in enumerate(ag_list): 
    if ag_var not in par.record_names:
        par_orig = par.get_record(orig_list[ind])
        par.add_record(name=ag_var, values=par_orig._values, dimensions=par_orig._dimensions, file_name=par_orig.file_name)

new_name = '../yampa/yampa.param'
for params in par.record_names: 
    new_record = par.get_record(params)
    new_record.file_name = new_name 

par.write() 
ctl.write(name='../yampa/yampa.control')

