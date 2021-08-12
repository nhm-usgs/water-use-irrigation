import subprocess
import os
import stat

    

def run_region(region_):
    exe = '/caldera/projects/usgs/water/wbeep/NHM/gf_v11/wu/gsflow/gsflow_v2/GSFLOW/bin/gsflow'
    ctl = 'control.default.bandit'
    region_name = str(region_).zfill(2)
    sh_name = region_name + '.sh'
    os.chdir('./20210730_v11_gm_r' + region_name)
    bash_script = open(sh_name, 'w')
    bash_script.write('#!/usr/bin/sh\n')
    bash_script.write(exe + ' ' + ctl)
    bash_script.close()
    st = os.stat(sh_name)
    os.chmod(sh_name, st.st_mode | stat.S_IEXEC) 
    subprocess.call('./'+sh_name) #, shell=True)
    os.chdir('..')

downstream_basins = [8, 15]
for basin in downstream_basins:
    run_region(basin)
