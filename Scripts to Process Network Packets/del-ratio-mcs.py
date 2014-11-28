import numpy as np
import matplotlib.pyplot as plt
from math import exp
import sys,string
from matplotlib.backends.backend_pdf import PdfPages
import csv

pp = PdfPages('del-ratio-mcs.pdf')

outfile = csv.writer(open("del-ratio-mcs.csv","w"), delimiter=',',lineterminator='\n')

file = open('datafile.csv','r')
lines = file.readlines()
file.close()
iterator = 1

MCS = [[]for _ in range(16)]
for x in range(0,16):    
    iterator = 1
    while(iterator < len(lines)):
        line = lines[iterator]
        values = string.split(line,',')
        trimmmed = values[5].replace('"','')
        if(trimmmed == 'mcs' + str(x)):
                    MCS[x].append(float(values[6]))
        iterator = iterator + 1
plt.suptitle('Delivery-Ratio vs MCS', fontsize=15)
plt.ylabel("Delivery Ratio")
  
plt.xlabel("MCS No")	
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15'],rotation=45)
plt.boxplot(MCS)
plt.ylim([0,1])	
plt.savefig(pp, format='pdf')
plt.clf()

####################################################################################################################################

def process(val):
	val = val.replace('"', '')
	val = val.replace('\n' , '')
	return val

link = {}
trial = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
iterator = 1
mcsValues = {}
trialValues = []
print 'reached for plotting the graph'
while(iterator < len(lines)):
        line = lines[iterator]
	values = string.split(line, ',')
	mcs = process(values[5])
	delratio = process(values[6])
	trial = process(values[2])
	lnk = process(values[7])
	if(lnk in link):
		mcsValues = link[lnk]
		if(mcs in mcsValues):
			trialValues = mcsValues[mcs]
		else:
			trialValues = []
	else:
		mcsValues = {}
		trialValues = []
	trialValues.append(float(delratio))
	mcsValues.update({mcs: trialValues})
	link.update({lnk: mcsValues})	
        iterator = iterator + 1	
outfile.writerow(['Link', 'MCS', 'Mean', 'Median', 'Standard Deviation'])
for lnk in link:
	data = []
	for x in range(0,16):
     		data.append(link[lnk][('mcs'+str(x))])
            	outfile.writerow([lnk, 'mcs'+str(x), np.mean(link[lnk][('mcs'+str(x))]), np.median(link[lnk][('mcs'+str(x))]), np.std(link[lnk][('mcs'+str(x))])])
	plt.suptitle('Delivery-Ratio vs MCS  ' + lnk, fontsize=15)
	plt.ylabel("Delivery Ratio")  
	plt.xlabel("MCS No")	
	plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],			  ['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15'],rotation=45)
	plt.scatter([i for i in range(0,16)],data, s= 80, marker='o')
	plt.ylim([0,1])	
	plt.savefig(pp, format='pdf')
	plt.clf()	
pp.close()	

