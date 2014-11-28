import matplotlib.pyplot as plt
from math import exp
import sys,string
from matplotlib.backends.backend_pdf import PdfPages
import csv
import numpy as np

pp = PdfPages('del-ratio-rssi.pdf')

outfile = csv.writer(open("del-ratio-rssi.csv","w"), delimiter=',',lineterminator='\n')

# rssi.csv is the file that will be generated after executing the datafile.py
file = open('rssi.csv','r')
lines = file.readlines()
file.close()
iterator = 1

rssiValues = [65,70,75,80,85,90,95]

lossValues = [[]for _ in range(7)]


while(iterator < len(lines)):
    line = lines[iterator]
    values = string.split(line,',')

    for x in range(0,7):
        
        if ((float(values[7]) < float(rssiValues[x])) and (float(values[7]) > (float(rssiValues[x]) - 5.0))):
            
            lossValues[x].append(float(values[8]))
    iterator = iterator + 1

##########################################Delivery-Ratio vs RSSI/Combined-All-MCS###################################
plt.suptitle('Delivery-Ratio vs RSSI/Combined-All-MCS', fontsize=15)
plt.ylabel("Delivery Ratio")	
plt.ylim([0,1])
plt.xlabel("RSSI")	
plt.xticks([0,1,2,3,4,5,6],['60-65','65-70','70-75','75-80','80-85','85-90','90-95'])
plt.boxplot(lossValues)
plt.savefig(pp, format='pdf')
plt.clf()

####################################################################################################################
##########################################Delivery-Ratio vs RSSI<70#################################################
lossMCS = [[]for _ in range(16)]
rssi = {}
for x in range(0,16):
    
    iterator = 1
    while(iterator < len(lines)):
        
        line = lines[iterator]
        values = string.split(line,',')
        trimmmed = values[6].replace('"','')
        if(trimmmed == 'mcs' + str(x)):

                if ((float(values[7]) < 70.0)):
            
                    lossMCS[x].append(float(values[8]))
        iterator = iterator + 1
    rssi.update({' < 70': lossMCS})
plt.suptitle('Delivery-Ratio vs RSSI < 70', fontsize=15)
plt.ylabel("Delivery Ratio")
  
plt.xlabel("RSSI")	
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15'],rotation=45)
plt.boxplot(lossMCS)
plt.ylim([0,1])	
plt.savefig(pp, format='pdf')
plt.clf()
#########################################################################################################################

##########################################Delivery-Ratio vs RSSI 70-80###################################################
lossMCS = [[]for _ in range(16)]
for x in range(0,16):
    
    iterator = 1
    while(iterator < len(lines)):
        
        line = lines[iterator]
        values = string.split(line,',')
        trimmmed = values[6].replace('"','')
        if(trimmmed == 'mcs' + str(x)):
            
                if ((float(values[7]) < 80.0) and (float(values[7]) > 70.0)):
            
                    lossMCS[x].append(float(values[8]))
        iterator = iterator + 1
    rssi.update({'70 - 80': lossMCS})
plt.suptitle('Delivery-Ratio vs RSSI 70-80', fontsize=15)
plt.ylabel("Delivery Ratio")
  
plt.xlabel("RSSI")	
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15'],rotation=45)
plt.boxplot(lossMCS)
plt.ylim([0,1])	
plt.savefig(pp, format='pdf')
plt.clf()

###########################################################################################################################

##########################################Delivery-Ratio vs RSSI 80-90########################################################
lossMCS = [[]for _ in range(16)]
for x in range(0,16):
    
    iterator = 1
    while(iterator < len(lines)):
        
        line = lines[iterator]
        values = string.split(line,',')
        trimmmed = values[6].replace('"','')
        if(trimmmed == 'mcs' + str(x)):
            
                if ((float(values[7]) < 90.0) and (float(values[7]) > 80.0)):
            
                    lossMCS[x].append(float(values[8]))
        iterator = iterator + 1
    rssi.update({'80 - 90': lossMCS})
plt.suptitle('Delivery-Ratio vs RSSI 80-90', fontsize=15)
plt.ylabel("Delivery Ratio")
  
plt.xlabel("RSSI")	
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15'],rotation=45)
plt.boxplot(lossMCS)
plt.ylim([0,1])	
plt.savefig(pp, format='pdf')
plt.clf()

################################################################################################################################

##########################################Delivery-Ratio vs RSSI > 90##########################################################
lossMCS = [[]for _ in range(16)]
for x in range(0,16):
    
    iterator = 1
    while(iterator < len(lines)):
        
        line = lines[iterator]
        values = string.split(line,',')
        trimmmed = values[6].replace('"','')
        if(trimmmed == 'mcs' + str(x)):
            
                if (float(values[7]) > 90.0):
            
                    lossMCS[x].append(float(values[8]))
        iterator = iterator + 1
    rssi.update({' > 90': lossMCS})
plt.suptitle('Delivery-Ratio vs RSSI > 90', fontsize=15)
plt.ylabel("Delivery Ratio")
  
plt.xlabel("RSSI")	
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['MCS0','MCS1','MCS2','MCS3','MCS4','MCS5','MCS6','MCS7','MCS8','MCS9','MCS10','MCS11','MCS12','MCS13','MCS14','MCS15'],rotation=45)
plt.boxplot(lossMCS)
plt.ylim([0,1])	
plt.savefig(pp, format='pdf')
plt.clf()
outfile.writerow(['RSSI', 'MCS', 'Mean', 'Median', 'Standard Deviation'])
for val in rssi:
	print rssi[val]
	for x in range(0,16):
		print x
		outfile.writerow([val, 'mcs'+str(x), np.mean(rssi[val][x]), np.median(rssi[val][x]), np.std(rssi[val][x])])
#################################################################################################################################
pp.close()
