import gsflow 
import numpy as np

region_list = [1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 16, 17, 18]
for region in region_list:
    region_name = '20210730_v11_gm_r' + str(region).zfill(2)
    print('processing region ' + region_name)
    orig_model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/regions/' + region_name
    new_model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/basins/' + region_name
    control_file = orig_model_dir+'/control.default.bandit'
    gs = gsflow.GsflowModel.load_from_file(control_file=control_file)
    ctl = gs.control 
    par = gs.prms.parameters
    for ctl_param in ctl.record_names:
        par_orig = ctl.get_record(ctl_param)
        if 'file' in par_orig.name and isinstance(par_orig._values[0], str):
            orig_path = par_orig._values[0].split('/')
            ctl.set_values(name=par_orig.name, values=[new_model_dir + '/' + orig_path[-1]])
    ctl.write(name=new_model_dir+'/control.default.bandit')
