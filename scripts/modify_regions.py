import gsflow 
import numpy as np

for r in range(18):
    region_name = '20210730_v11_gm_r' + str(r+1).zfill(2)
    print('processing region ' + region_name)
    model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/regions/' + region_name
    control_file = model_dir+'/control.default.bandit'
    gs = gsflow.GsflowModel.load_from_file(control_file=control_file)
    ctl = gs.control 
    par = gs.prms.parameters
    mod_par = gsflow.prms.PrmsParameters(parameters_list=[])
    
    mod_filename = 'mod.param'
    for params in par.record_names:
        if 'poi_gage_id' not in params:
            par_orig = par.get_record(params)
            mod_par.add_record(name=par_orig.name, values=par_orig._values, dimensions=par_orig._dimensions, file_name=model_dir + '/' + mod_filename)
    ctl.set_values(name='param_file', values=[mod_filename])
    ctl.write()
    mod_par.write()
