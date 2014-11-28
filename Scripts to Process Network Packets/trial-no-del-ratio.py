import matplotlib.pyplot as plt
from math import exp
import re
import sys,string
from matplotlib.backends.backend_pdf import PdfPages

file = open('trial-no-vs-del-ratio-2.csv','r')
lines = file.readlines()
file.close()

pp = PdfPages('multipage3.pdf')

link = {}
mcs = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15}
iterator = 1
while(iterator < len(lines)):
        
        line = lines[iterator]
        values = string.split(line,',')
        trimmed = values[7].replace('"','')
        trimmed = trimmed.replace('\n','')
        link.update({trimmed:0})
        iterator = iterator + 1

count = 0
for x in link:
    iterator = 1
    print x
    dataset = [{}for _ in range(10)]
    while(iterator < len(lines)):
        line = lines[iterator]
        values = string.split(line,',')
        trimmedLink = values[7].replace('"','')
        trimmedLink = trimmedLink.replace('\n','')
        trimmedMcs = values[5].replace('"','')
        val = re.search(r'\d+',trimmedMcs).group()
        for key in range(0,10):
            if (trimmedLink == x and key == int(values[2])):
				#plt.plot(int(values[2]),float(values[6]))
				dataset[key].update({int(val):float(values[6])})
        iterator = iterator + 1
    finaldata=[[]for _ in range(10)]
    for num in range(0,10):
        for mcs in range(0,16):
            finaldata[num].append((dataset[num]).get(mcs,0))
    print finaldata	
    for y in range(0,10):		
        plt.plot(finaldata[y])	
    plt.suptitle(x, fontsize=15)
    plt.xlabel("Trial No")
    plt.ylabel("Delivery Ratio")
    plt.savefig(pp, format='pdf')
    plt.clf()
pp.close()    


