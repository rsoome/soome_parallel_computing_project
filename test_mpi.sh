#!/bin/bash

##The job should run on the testing partition
#SBATCH --partition=main

##The name of the job is test_job
#SBATCH -J mpi_test

##The job requires 4 compute nodes
#SBATCH --cpus-per-task=10

##The job requires 1 task per node
#SBATCH --ntasks-per-node=1

##The maximum walltime of the job is a half hour
#SBATCH --time=240

##Mem
#SBATCH --mem=10G

##These commands are run on one of the nodes allocated to the job (batch node)
module load python-3.7.1
source imgproc/bin/activate
module load openmpi-3.1.0 
echo "mpirun --oversubscribe -n %%CPUS python pympi.py no_of_files=%%FILES"
mpirun --oversubscribe -n 10 python pympi.py no_of_files=100
uname -a
