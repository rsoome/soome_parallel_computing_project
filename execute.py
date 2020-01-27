import subprocess

scripts = ["run_mpi.sh", "run_pymp.sh", "run_mpi1.sh", "run_pymp1.sh"]
to_run = []

for script in scripts:
    with open(script, "r") as f:
        to_run.append(f.read())

for cpus in range(5,21,5):
    no_of_files = 1
    while no_of_files < 1000000:
        for running in to_run:
            ps = subprocess.Popen("sbatch << EOF\n" + running.replace("%%CPUS", str(cpus)).replace("%%FILES", str(no_of_files)) + "\nEOF", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = ps.communicate()
            print(out)
            print(err)
        no_of_files *= 10
