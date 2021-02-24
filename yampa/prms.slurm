#!/bin/bash

#SBATCH --job-name=prms-nhm
#SBATCH --output=%j-prms-nhm.out
#SBATCH -n 1
#SBATCH --hint=nomultithread
#SBATCH --time=20:00:00
#SBATCH --account=cawsc
#SBATCH --mail-type=END
#SBATCH --mail-user=mrush@usgs.gov

module swap PrgEnv-cray PrgEnv-gnu
srun ./prms.sh
