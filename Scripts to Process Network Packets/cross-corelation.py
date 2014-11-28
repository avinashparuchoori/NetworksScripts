import matplotlib.pyplot as plt
from math import exp
import re
import sys,string
from matplotlib.backends.backend_pdf import PdfPages
import math
import numpy as np
import scipy
import random

file = open('datafile.csv','r')
lines = file.readlines()
file.close()

pp = PdfPages('multipage6.pdf')

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
#print link
del link["105-118"]
del link["106-114"]
del link["111-115"]
del link["112-103"]
del link["105-107"]
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
        if len(mcsValues) == 10: #check if link has all trials
            linkVal=[]
            for y in range(0,10):
                linkVal.append(mcsValues[y])
            linkValues.append(linkVal)
    dataset.update({lnk:linkValues})
#print dataset

'''
def co_relation(x_array,y_array):  # main function
    ans = 0.0
    x_mean_values=[]               # stores x - mean(x)
    y_mean_values=[]               # stores y - mean(y)
    final_values = []
    sum_final = 0.0
    sum_x = 0.0
    sum_y = 0.0    
    for x in range(0,10):
        x_mean_values.append(np.subtract(x_array[x],np.mean(x_array)))
        y_mean_values.append(np.subtract(y_array[x],np.mean(y_array)))
    #print x_mean_values
    #print y_mean_values 
       
    for x in range(0,10):
        final_values.append(np.multiply(x_mean_values[x],y_mean_values[x])) # x-mean(x) * y-mean(y)
    for x in range(0,10):
        sum_final = np.add(sum_final,final_values[x])   # add(x-mean(x) * y-mean(y))
    ##print sum_final
    for x in range(0,10):
        sum_x = np.add(sum_x,np.power(x_mean_values[x],2))
    #print sum_x
    for x in range(0,10):
        sum_y = np.add(sum_y,np.power(y_mean_values[x],2))
    #print sum_y
    ans = np.divide(sum_final,np.multiply(np.sqrt(sum_x),np.sqrt(sum_y)))
    return ans

def co_variance(x_array,y_array):  # main function
    ans = 0.0
    x_mean_values=[]               # stores x - mean(x)
    y_mean_values=[]               # stores y - mean(y)
    final_values = []
    sum_final = 0.0
    sum_x = 0.0
    sum_y = 0.0    
    for x in range(0,10):
        x_mean_values.append(np.subtract(x_array[x],np.mean(x_array)))
        y_mean_values.append(np.subtract(y_array[x],np.mean(y_array)))
    #print x_mean_values
    #print y_mean_values 
       
    for x in range(0,10):
        final_values.append(np.multiply(x_mean_values[x],y_mean_values[x])) # x-mean(x) * y-mean(y)
    for x in range(0,10):
        sum_final = np.add(sum_final,final_values[x])   # add(x-mean(x) * y-mean(y))
    ##print sum_final
    for x in range(0,10):
        sum_x = np.add(sum_x,np.power(x_mean_values[x],2))
    #print sum_x
    for x in range(0,10):
        sum_y = np.add(sum_y,np.power(y_mean_values[x],2))
    print sum_final
    ans = np.divide(sum_final,9)
    return ans

def np_co_relation(x_array,y_array):
    ans = 0.0
    x_mean_values=[]               # stores x - mean(x)
    y_mean_values=[]               # stores y - mean(y)
    final_values = []
    sum_final = 0.0
    max_x = max(x_array)
    #print sum_x
    max_y = max(y_array)    
    for x in range(0,10):
        x_mean_values.append(np.subtract(max_x,x_array[x]))
        y_mean_values.append(np.subtract(max_y,y_array[x]))
    
    return (np.correlate(x_mean_values,y_mean_values))'''

def gaussian_distance(x_array,y_array):
    ans = 0.0
    diff=[]               # stores x - mean(x)
    total = 0.0
    sigma = np.power((np.log(16)/16),10)
    for x in range(0,10):
        diff.append(np.subtract(x_array[x],y_array[x]))
    for x in range(0,10):
        diff[x] = np.power(diff[x],2)
    for x in range(0,10):    
        total = total + diff[x]
   
    
    return math.exp(np.divide(-total,np.multiply(2,np.power(0.3,2))))

def average_delratio(x_array):
    ans = 0.0
    for x in range(0,10):    
        ans = ans + x_array[x]
    return np.divide(ans,10)

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

finalset={} # graph 1 - correlation between same modulation types
for lnk in dataset:
    linkValues = {}
    #print '----------------'+lnk+'----------------'
    for y in range (0,16):
        for z in range(y+1,16):
       
            gau = gaussian_distance(dataset[lnk][y],dataset[lnk][z])
            
            mcs = 'MCS' + str(y) + '-' + 'MCS' + str(z)
            linkValues.update({mcs:gau})
            #if (gau > 0.8):
                #print  mcs +':' + str(linkValues[mcs] ) + '-----mcs' + str(y) + ':' + str(average_delratio(dataset[lnk][y])) + '------mcs' + str(z) + ':' + str(average_delratio(dataset[lnk][z])) + '------eucledian distance:' + str(eucledian_distance(dataset[lnk][y],dataset[lnk][z]))
    finalset.update({lnk:linkValues})
print finalset


for lnk in finalset:
    counter = 1
    for y in range (0,16):
        for z in range(y+1,16):
            counter = counter + 1
            mcs = 'MCS' + str(y) + '-' + 'MCS' + str(z)
            plt.plot(counter,finalset[lnk][mcs],'ro',markersize=0.5)
plt.suptitle('Gaussian Similarity', fontsize=15)
plt.ylim(0,1)
plt.xlim(0,121)
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121],['MCS0-MCS1','MCS0-MCS2','MCS0-MCS3','MCS0-MCS4','MCS0-MCS5','MCS0-MCS6','MCS0-MCS7','MCS0-MCS8','MCS0-MCS9','MCS0-MCS10','MCS0-MCS11','MCS0-MCS12','MCS0-MCS13','MCS0-MCS14','MCS0-MCS15','MCS1-MCS2','MCS1-MCS3','MCS1-MCS4','MCS1-MCS5','MCS1-MCS6','MCS1-MCS7','MCS1-MCS8','MCS1-MCS9','MCS1-MCS10','MCS1-MCS11','MCS1-MCS12','MCS1-MCS13','MCS1-MCS14','MCS1-MCS15','MCS2-MCS3','MCS2-MCS4','MCS2-MCS5','MCS2-MCS6','MCS2-MCS7','MCS2-MCS8','MCS2-MCS9','MCS2-MCS10','MCS2-MCS11','MCS2-MCS12','MCS2-MCS13','MCS2-MCS14','MCS2-MCS15','MCS3-MCS4','MCS3-MCS5','MCS3-MCS6','MCS3-MCS7','MCS3-MCS8','MCS3-MCS9','MCS3-MCS10','MCS3-MCS11','MCS3-MCS12','MCS3-MCS13','MCS3-MCS14','MCS3-MCS15','MCS4-MCS5','MCS4-MCS6','MCS4-MCS7','MCS4-MCS8','MCS4-MCS9','MCS4-MCS10','MCS4-MCS11','MCS4-MCS12','MCS4-MCS13','MCS4-MCS14','MCS4-MCS15','MCS5-MCS6','MCS5-MCS7','MCS5-MCS8','MCS5-MCS9','MCS5-MCS10','MCS5-MCS11','MCS5-MCS12','MCS5-MCS13','MCS5-MCS14','MCS5-MCS15','MCS6-MCS7','MCS6-MCS8','MCS6-MCS9','MCS6-MCS10','MCS6-MCS11','MCS6-MCS12','MCS6-MCS13','MCS6-MCS14','MCS6-MCS15','MCS7-MCS8','MCS7-MCS9','MCS7-MCS10','MCS7-MCS11','MCS7-MCS12','MCS7-MCS13','MCS7-MCS14','MCS7-MCS15','MCS8-MCS9','MCS8-MCS10','MCS8-MCS11','MCS8-MCS12','MCS8-MCS13','MCS8-MCS14','MCS8-MCS15','MCS9-MCS10','MCS9-MCS11','MCS9-MCS12','MCS9-MCS13','MCS9-MCS14','MCS9-MCS15','MCS10-MCS11','MCS10-MCS12','MCS10-MCS13','MCS10-MCS14','MCS10-MCS15','MCS11-MCS12','MCS11-MCS13','MCS11-MCS14','MCS11-MCS15','MCS12-MCS13','MCS12-MCS14','MCS12-MCS15','MCS13-MCS14','MCS13-MCS15','MCS14-MCS15'],rotation=90,fontsize=4)
plt.savefig(pp, format='pdf')
plt.clf()
pp.close()

for y in range (0,16):
        for z in range(y+1,16):
            
            mcs = 'MCS' + str(y) + '-' + 'MCS' + str(z)
            print mcs

#print finalset
        #cor = np_co_relation(dataset[x][y],dataset[x+8][y])
        #print cor
        #plt.plot(x+1,cor,'ro')
        #plt.plot(x+1,np.correlate((dataset[x][y]),(dataset[x+8][y])),"ro")
#print finalset
#plt.scatter(finalset)
#plt.suptitle('Covariance', fontsize=15)
#plt.ylabel("Correlation Value")

#plt.xlim(0,9)
#plt.ylim(-1,1.1)
#plt.savefig(pp, format='pdf')
#plt.clf()
#print finalset['111-102']

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
    
#k means clustering    
'''for lnk in finalset:
    #if lnk == '102-120':
        values={}    
        centeroid =[]
        for y in range (0,16):
            for z in range(y+1,16):
                count = 0
                mcs = 'MCS' + str(y) + '-' + 'MCS' + str(z)
                values.update({mcs:finalset[lnk][mcs]})
        #print values
        centeroid = getRandom(values)
        #print centeroid
        #print values
        lnkCenteroidCluster = getValuesForCenteroid(centeroid,values)
        var = 1
        while var == 1:
            flag = 0;   
            for x in range(0,len(centeroid)):
                newCenteroid = getMedian(lnkCenteroidCluster[centeroid[x]])
                if(abs(newCenteroid - centeroid[x]) < .005):
                    flag = flag + 1
                    #print newCenteroid
                    #print centeroid[x]
                else: 
                    centeroid[x] = newCenteroid
            if (flag < 8):
               lnkCenteroidCluster.clear()
               lnkCenteroidCluster = getValuesForCenteroid(centeroid,values)
            else:   
                break
        print '-----------' + lnk + '----------'
        for center in lnkCenteroidCluster:
            print '+++++++++++' + str(center) + '+++++++++++'
            for u in range (0,16):
                for v in range(u+1,16):            
                    mcs1 = 'MCS' + str(u) + '-' + 'MCS' + str(v)
                    
                    if mcs1 in lnkCenteroidCluster[center]:
                        print mcs1  + ':' + str(lnkCenteroidCluster[center][mcs1])'''






'''finalset1=[[]for _ in range (7)] # graph corelation between adjacent MCS 0-7
for x in range (0,7):
    for y in range (0,20):
        cor = co_relation(dataset[x][y],dataset[x+1][y])
        plt.plot(x+1,cor,'bo')
        cor = np_co_relation(dataset[x][y],dataset[x+1][y])
        plt.plot(x+1,cor,'ro')
        #plt.plot(x+1,(np.correlate(dataset[x][y],dataset[x+1][y])),"ro")
#plt.boxplot(finalset1)
plt.suptitle('Cross-Correlation-1', fontsize=15)
plt.ylabel("Correlation Value")
plt.xticks([1,2,3,4,5,6,7],['MCS0-1','MCS1-2','MCS2-3','MCS3-4','MCS4-5','MCS5-6','MCS6-7'],rotation=30)
plt.xlim(0,8)
plt.ylim(-1,1.1)
plt.savefig(pp, format='pdf')
plt.clf()

finalset2=[[]for _ in range (7)]# graph corelation between adjacent MCS 8-15
for x in range (8,15):
    for y in range (0,20):
        cor = co_relation(dataset[x][y],dataset[x+1][y])
        plt.plot(x+1,cor,'bo')
        cor = np_co_relation(dataset[x][y],dataset[x+1][y])
        plt.plot(x+1,cor,'ro')
#plt.boxplot(finalset2)

plt.suptitle('Cross-Correlation-2', fontsize=15)
plt.ylabel("Correlation Value")
plt.xticks([9,10,11,12,13,14,15],['MCS8-9','MCS9-10','MCS10-11','MCS11-12','MCS12-13','MCS13-14','MCS14-15'],rotation=30)
plt.xlim(8,16)
plt.ylim(-1,1.1)
plt.savefig(pp, format='pdf')
plt.clf()
pp.close()'''


