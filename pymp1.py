import cv2
import numpy as np
import threading
import time
from multiprocessing import Pool
import sys


args = {'no_of_threads': 10, 'no_of_files': 0, 'threshold': 100}

with open('./filelist') as f:
    srcfiles = f.read()
asrcfiles = srcfiles.split()

args['no_of_files'] = len(asrcfiles)
divider = 1

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
                with Pool(no_of_threads) as p:
                    results = p.map(avg, splitimg)
                    average = np.sum(results)
                if average > args['threshold']:
                        vf.append(sfile) 
                tot_time += time.time() - start

    vf.append(iterations)
    vf.append(tot_time)

    return vf

start = time.time()
results = filter_images()
end = time.time()

tot_iterations = results[-2]
tot_time = results[-1]
ips = float(tot_time)/tot_iterations

output = ''
with open('./results/pymp1_results' + '_' + str(args['no_of_threads']) + 'thr_' + str(min(len(asrcfiles), args['no_of_files'])) + 'files' , 'w+') as f:
    output += str(args['no_of_threads']) + ' ' + str(args['no_of_files']) + ' ' +  str(end - start) + ' ' + str(ips) + '\n'
    for i in range(len(results) - 2):
        j = results[i]
        output += j + '\n'
    
    f.write(output)
