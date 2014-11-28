import matplotlib.pyplot as plt
from math import exp
import re
import sys,string
from matplotlib.backends.backend_pdf import PdfPages
import math
import numpy as np
import scipy
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as hier
import random

file = open('datafile.csv','r')
lines = file.readlines()
file.close()

def process(val):
	val = val.replace('"', '')
	val = val.replace('\n' , '')
	return val

pp = PdfPages('per-node-hierarchial-clustering-normalized-complete.pdf')

source = {}
trial = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
iterator = 1
while(iterator < len(lines)):
        line = lines[iterator]
        values = string.split(line,',')
        trimmed = values[4].replace('"','')
        trimmed = trimmed.replace('\n','')
        source.update({trimmed:0})
        iterator = iterator + 1
print source
print len(source)
'''del link["105-118"]
del link["106-114"]
del link["111-115"]
del link["112-103"]
del link["105-107"]'''

dataset = {}
dictmcs = {}
dicttrial = {}
listtrial = []
iterator = 1
while(iterator < len(lines)):
	line = lines[iterator]
	values = string.split(line, ',')
	mcs = process(values[5])
	delratio = process(values[6])
	trial = process(values[2])
	src = process(values[4])
	if(src in dataset):
		dictmcs = dataset[src]
		if(mcs in dictmcs):
			dicttrial = dictmcs[mcs]
			if(trial in dicttrial):
				listtrial = dicttrial[trial]
			else:
				listtrial = []
		else:
			dicttrial = {}
			listtrial = []
	else:
		dictmcs = {}
		dicttrial = {}
		listtrial = []
	listtrial.append(float(delratio))
	dicttrial.update({trial:listtrial})
	dictmcs.update({mcs:dicttrial})
	dataset.update({src:dictmcs})
	iterator = iterator + 1
		

	

rowHeaders=['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15']
colHeaders=[1,2,3,4,5,6,7,8,9,10]
data = {}

for src in dataset:
	mcsvals = []
	for m in range(0,16):
		trialvals = []
		for t in range(1, 2):
			key = 'mcs'+str(m)		
			trialvals.append(np.mean(dataset[src][key][str(t)]))
		mcsvals.append(trialvals)
	data.update({src:mcsvals})

for src in data:
    dataMatrix = np.array(data[src]) 
    #print dataMatrix

    distanceMatrix = dist.pdist(dataMatrix,'euclidean')
    #print distanceMatrix
    
    distanceMatrix = distanceMatrix
    
    linkageMatrix = hier.linkage(distanceMatrix,method='complete')
    #print linkageMatrix

    #heatmapOrder = hier.leaves_list(linkageMatrix)
    #print heatmapOrder
    T = hier.to_tree( linkageMatrix , rd=False )

    hier.dendrogram(linkageMatrix, orientation='top')
    #plt.savefig("scipy-dendrogram" + lnk + ".png")
    plt.xlabel("MCS No")
    plt.ylabel("Distance")
    plt.suptitle(src, fontsize=15)
    plt.savefig(pp, format ='pdf')
    plt.clf()
pp.close()
