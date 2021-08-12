#!/bin/bash

#SBATCH --job-name=prms-nhm
#SBATCH --output=%j-prms-nhm.out
#SBATCH -n 1
#SBATCH --hint=nomultithread
#SBATCH --time=20:00:00
#SBATCH --account=cawsc

module swap PrgEnv-cray PrgEnv-gnu
#scripts that modify model:
python modify_paths.py
python modify_upstream.py
python modify_downstream.py
#scripts that run model:
python run_upstream_basins.py
python move_mississippi.py
python move_colorado.py
python run_downstream_basins.py
