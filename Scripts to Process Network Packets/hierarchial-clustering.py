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

pp = PdfPages('hierarchial-clustering-normalized-average.pdf')

link = {}
trial = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
iterator = 1
while(iterator < len(lines)):
        line = lines[iterator]
        values = string.split(line,',')
        trimmed = values[7].replace('"','')
        trimmed = trimmed.replace('\n','')
        link.update({trimmed:0})
        iterator = iterator + 1
print link
print len(link)
'''del link["105-118"]
del link["106-114"]
del link["111-115"]
del link["112-103"]
del link["105-107"]'''
dataset = {} #loop through all MCS
count = 0
for lnk in link:  # loop through each link in MCS
    linkValues = []   
    for x in range(0,16):    
        mcsValues = {}        
        iterator = 1    
        while(iterator < len(lines)):
            line = lines[iterator]
            values = string.split(line,',')
            trimmedLink = values[7].replace('"','')
            trimmedLink = trimmedLink.replace('\n','')
            trimmedMcs = values[5].replace('"','')
            if (trimmedLink == lnk and ('mcs' + str(x)) == trimmedMcs): # check link and add values to list
		    	mcsValues.update({int(values[2]):float(values[6])})
            iterator = iterator + 1
        #print lnkValues
        #if len(mcsValues) == 10: #check if link has all trials
        linkVal=[]
            #for y in range(0,10):
        for obj in mcsValues:
            linkVal.append(mcsValues[obj])
        linkValues.append(linkVal)
    dataset.update({lnk:linkValues})

'''datasetfinal = {}
for lnk in dataset:
    linkValues = []
    for y in range(0,10):
        trialValues = []
        for x in range(0,16):
            trialValues.append(dataset[lnk][x][y])
        linkValues.append(trialValues)
    datasetfinal.update({lnk:linkValues})'''

rowHeaders=['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15']
colHeaders=[1,2,3,4,5,6,7,8,9,10]

for lnk in dataset:

    dataMatrix = np.array(dataset[lnk]) 
    if(lnk == '102-120'):
	print dataset[lnk]
    #print dataMatrix
    print lnk
    if(lnk == '116-108'):
        print dataMatrix
    distanceMatrix = dist.pdist(dataMatrix, 'euclidean')
    #print distanceMatrix


    distanceMatrix = distanceMatrix
    
    linkageMatrix = hier.linkage(distanceMatrix,method='average')
    #print linkageMatrix

    #heatmapOrder = hier.leaves_list(linkageMatrix)
    #print heatmapOrder
    T = hier.to_tree( linkageMatrix , rd=False )

    hier.dendrogram(linkageMatrix, orientation='top')
    #plt.savefig("scipy-dendrogram" + lnk + ".png")
    plt.xlabel("MCS No")
    plt.ylabel("Distance")
    plt.suptitle(lnk, fontsize=15)
    plt.savefig(pp, format ='pdf')
    plt.clf()
pp.close()
#orderedDataMatrix = dataMatrix[heatmapOrder,:]
#print orderedDataMatrix
#rowHeaders = np.array(rowHeaders)
#orderedRowHeaders = rowHeaders[heatmapOrder,:]
#matrixOutput = []
#row = 0
'''for rowData in orderedDataMatrix:
	col = 0
	rowOutput = []
	for colData in rowData:
		rowOutput.append([colData, row, col])
		col += 1
	matrixOutput.append(rowOutput)
	row += 1

print 'var maxData = ' + str(np.amax(dataMatrix)) + ";"
print 'var minData = ' + str(np.amin(dataMatrix)) + ";"
print 'var data = ' + str(matrixOutput) + ";"
print 'var cols = ' + str(colHeaders) + ";"
print 'var rows = ' + str([x for x in orderedRowHeaders]) + ";"'''

def eucledian_distance(x_array,y_array):
    ans = 0.0
    diff=[]               # stores x - mean(x)
    total = 0.0
    
    for x in range(0,10):
        diff.append(np.subtract(x_array[x],y_array[x]))
    for x in range(0,10):
        diff[x] = np.power(diff[x],2)
    for x in range(0,10):    
        total = total + diff[x]
    return np.sqrt(total)


def getValuesForCenteroid(centeroid, array):
        centeroidList = {}
        for a in range(0,len(centeroid)):
            #print a
            centeroidList.update({centeroid[a]:{}})      
     
        for x in array:
            centeroid_distance = []

            for y in range(0,len(centeroid)):
                centeroid_distance.append(abs(centeroid[y] - array[x]))
            minimum = centeroid_distance[0]
            minIndex = 0        
            for z in range(1,len(centeroid_distance)):
                    if(minimum > centeroid_distance[z]):
                        minimum = centeroid_distance[z]        
                        minIndex = z
            centeroidList[centeroid[minIndex]].update({x:array[x]})        
        return centeroidList
        
def getRandom(dictionary):
    values=[]
    centeroid = []
    for val in dictionary:   
        values.append(dictionary[val])
    for counter in range (0,8):
        centeroid.append(random.choice(values))
    return centeroid

def getMedian(dictionary):
    values=[]
    for val in dictionary:   
        values.append(dictionary[val])
    median = np.median(values)
    return median
 

