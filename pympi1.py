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

divider = 1

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
def avg(arrays):
    global divider
    tot = np.sum(arrays)
    #if arrays[arrays.shape[0] - 1][arrays.shape[1] - 1][arrays.shape[2] - 1] == -1:
    #    sum += np.sum(arrays[arrays.shape[0] - 1])
    return tot/divider

def filter_images():

    global asrcfiles
    global args
    global arrlen
    global rank
    global divider
    vf = []

    no_of_threads = args['no_of_threads']
    no_of_files = args['no_of_files']
    splitimg = None
    iterations = 0
    tot_time = 0
    for i in range(no_of_files):
        if i >= len(asrcfiles):
            break

        sfile = asrcfiles[i]
        if 'jpg' in sfile:
                iterations += 1 
                subj = cv2.imread(sfile)
                start = time.time()
                divider = np.prod(subj.shape)
                
                splitimg = np.array_split(subj,no_of_threads,0)

                #for j in range(subj.shape[0]):
                #    splitimg[j%no_of_threads][j//no_of_threads] = subj[j]
                    
                average = 0
                if rank != 0:
                    result = avg(splitimg[rank])
                    comm.send(result, dest=0, tag=0)
                else: 
                    average = avg(splitimg[rank])
                    for i in range(1, size):
                        average += comm.recv(source=i, tag=0)
                    if average > args['threshold']:
                            vf.append(sfile) 
                    tot_time += time.time() - start
    if rank == 0:
        vf.append(iterations)
        vf.append(tot_time)

    return vf

start = time.time()
results = filter_images()
if rank == 0:
    end = time.time()
    ips = float(results[-1])/results[-2]
    
    output = ''
    with open('./results/pympi1_results' + '_' + str(args['no_of_threads']) + 'thr_' + str(min(len(asrcfiles), args['no_of_files'])) + 'files' , 'w+') as f:
        output += str(args['no_of_threads']) + ' ' + str(args['no_of_files']) + ' ' +  str(end - start) + ' ' + str(ips) + '\n'
        for i in range(len(results) - 2):
            j = results[i]
            output += j + '\n'
        
        f.write(output)
