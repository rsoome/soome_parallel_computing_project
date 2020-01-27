from mpi4py import MPI
import cv2
import numpy as np
import time
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

args = {'no_of_threads': 10, 'no_of_files': 0, 'threshold': 100}

args['no_of_threads'] = size

with open('./filelist') as f:
    srcfiles = f.read()
asrcfiles = srcfiles.split()

args['no_of_files'] = len(asrcfiles)

for arg in sys.argv:
    argsplit = arg.split('=')
    if len(argsplit) > 1:
        try:
            args[argsplit[0]] = int(argsplit[1])
        except:
            args[argsplit[0]] = argsplit[1]
        

arrlen = 0
gvf = []

def filter_images(startindex):

    global asrcfiles
    global args
    vf = []

    no_of_threads = args['no_of_threads']
    no_of_files = args['no_of_files']
    iterations = 0
    tot_time = 0
    for i in range(startindex,no_of_files,no_of_threads):
        if i >= len(asrcfiles):
            break
        sfile = asrcfiles[i]
        if 'jpg' in sfile:
                iterations += 1
                subj = cv2.imread(sfile)
                start = time.time()
                if np.average(subj) > args['threshold']:
                        vf.append(sfile) 
                tot_time += time.time() - start
    vf.append(iterations)
    vf.append(tot_time)

    return vf
    #gvf.append(vf)

results = []
start = time.time()

if rank != 0:
    result = filter_images(rank)
    comm.send(result, dest=0, tag=0)
else:
    result = filter_images(rank)
    results.append(result)
    for i in range(1, size):
        results.append(comm.recv(source=i, tag=0))

    end = time.time()
    
    tot_iterations = 0
    tot_time = 0
    
    for result in results:
        print(result[-2])
        print(result[-1])
        if len(result) - 2 > arrlen:
            arrlen = len(result) - 2
        tot_iterations += result[-2]
        tot_time += result[-1]
    
    ips = float(tot_time)/tot_iterations
    
    output = ''
    with open('./results/mpi_results' + '_' + str(args['no_of_threads']) + 'thr_' + str(min(len(asrcfiles), args['no_of_files'])) + 'files' , 'w+') as f:
        output += str(args['no_of_threads']) + ' ' + str(args['no_of_files']) + ' ' +  str(end - start) + ' ' + str(ips) + '\n'
        for i in range(arrlen):
            for j in results:
                if i >= len(j) - 2:
                    break
                output += j[i] + '\n'
            
        f.write(output)
