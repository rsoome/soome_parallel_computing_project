#!/bin/bash

##The job should run on the testing partition
#SBATCH --partition=main

##The name of the job is test_job
#SBATCH -J test

##The job requires 4 compute nodes
#SBATCH --cpus-per-task=%%CPUS

##The job requires 1 task per node
#SBATCH --ntasks-per-node=1

##The maximum walltime of the job is a half hour
#SBATCH --time=240

##These commands are run on one of the nodes allocated to the job (batch node)
echo "python3 pymp.py no_of_files=%%FILES no_of_threads=%%CPUS"
python3 pymp.py no_of_files=%%FILES no_of_threads=%%CPUS
uname -a
