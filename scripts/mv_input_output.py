import gsflow 
import numpy as np
import os

for r in range(18):
    region_name = '20210730_v11_gm_r' + str(r+1).zfill(2)
    print('processing region ' + region_name)
    model_dir = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/water-use-irrigation/regions/' + region_name
    os.makedir(os.path.join(model_dir, 'input'))
    os.makedir(os.path.join(model_dir, 'output'))
    os.rename(os.path.join(model_dir, 'tmin.cbh'), os.path.join(model_dir, 'input', 'tmin.cbh'))
    os.rename(os.path.join(model_dir, 'tmin.cbh'), os.path.join(model_dir, 'input', 'tmax.cbh'))
    os.rename(os.path.join(model_dir, 'tmin.cbh'), os.path.join(model_dir, 'input', 'prcp.cbh'))

