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
    global arrlen
    vf = []

    no_of_threads = args['no_of_threads']
    no_of_files = args['no_of_files']
    iterations = 0
    tot_time = 0
    for i in range(startindex,no_of_files,no_of_threads):
        if i >= len(asrcfiles):
            break
        sfile = asrcfiles[i]
        if i%100 <= no_of_threads:
            print(startindex, i, end='\r')
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
with Pool(args['no_of_threads']) as p:
    results = p.map(filter_images, list(range(args['no_of_threads'])))
end = time.time()

tot_iterations = 0
tot_time = 0

for result in results:
    if len(result) - 2 > arrlen:
        arrlen = len(result) - 2
    tot_iterations += result[-2]
    tot_time += result[-1]
ips = float(tot_time)/tot_iterations



output = ''
with open('./results/pymp_results' + '_' + str(args['no_of_threads']) + 'thr_' + str(min(len(asrcfiles), args['no_of_files'])) + 'files' , 'w+') as f:
    output += str(args['no_of_threads']) + ' ' + str(args['no_of_files']) + ' ' +  str(end - start) + ' ' +  str(ips) + '\n'
    for i in range(arrlen):
        for j in results:
            if i >= len(j) - 2:
                break
            output += j[i] + '\n'
        
    f.write(output)
