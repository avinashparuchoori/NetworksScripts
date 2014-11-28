import matplotlib.pyplot as plt
from math import exp
import re
import sys,string
from matplotlib.backends.backend_pdf import PdfPages
import math

file = open('datafile.csv','r')
lines = file.readlines()
file.close()

pp = PdfPages('multipage4.pdf')

link = {}
trial = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
iterator = 1
while(iterator < len(lines)):
        line = lines[iterator]
  	#print string.split(lines[0],',')   #['Tx retry', 'Destination', 'Number', 'Tx Success', 'Source', 'MCS\n']   
	values = string.split(line,',')
        trimmed = values[7].replace('"','')
        trimmed = trimmed.replace('\n','')
        link.update({trimmed:0})
        iterator = iterator + 1
dataset = [[]for _ in range(16)] #loop through all MCS
count = 0
for x in range(0,16): # loop through each MCS
    for lnk in link:  # loop through each link in MCS
        lnkValues = {}
        iterator = 1       
        while(iterator < len(lines)):        
            line = lines[iterator]
            values = string.split(line,',')
            trimmedLink = values[7].replace('"','')
            trimmedLink = trimmedLink.replace('\n','')
            trimmedMcs = values[5].replace('"','')
            if (trimmedLink == lnk and ('mcs' + str(x)) == trimmedMcs): # check link and add values to list
		    	lnkValues.update({int(values[2]):float(values[6])})
            iterator = iterator + 1
        if len(lnkValues) == 10: #check if link has all trials
            divValues = []
            sigma = 0.0
            for y in range(1,10): #calculate allendeviation for 10 trials
                divValues.append(math.pow(lnkValues[y] - lnkValues[y-1],2))        
            for z in range(0,9):
                sigma = sigma + divValues[z]
            dataset[x].append(math.sqrt(sigma/10)) #add allendeviation to list
plt.boxplot(dataset)
plt.suptitle('Allen Deviation vs MCS', fontsize=15)
plt.ylabel("Allen Deviation")
plt.ylim([0,0.5])	
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15'],rotation=60)
plt.savefig(pp, format='pdf')
pp.close()   


