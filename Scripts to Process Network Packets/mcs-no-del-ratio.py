import matplotlib.pyplot as plt
from math import exp
import re
import sys,string
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

file = open('datafile.csv','r')
lines = file.readlines()
file.close()

pp = PdfPages('mcs-no-del-ratio.pdf')

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

count = 0
for x in link:
    iterator = 1
    #print x
    dataset = [{}for _ in range(16)]
    while(iterator < len(lines)):
        line = lines[iterator]
        values = string.split(line,',')
        trimmedLink = values[7].replace('"','')
        trimmedLink = trimmedLink.replace('\n','')
        trimmedMcs = values[5].replace('"','')
        val = re.search(r'\d+',trimmedMcs).group()
        for key in range(0,16):
            if (trimmedLink == x and ('mcs' + str(key)) == trimmedMcs):
				#plt.plot(int(values[2]),float(values[6]))
				dataset[key].update({int(values[2]):float(values[6])})
        iterator = iterator + 1
    #print dataset		
	#plt.boxplot(dataset)
    finaldata=[[]for _ in range(16)]
    for mcs in range(0,16):
        for trial in range(0,10):
            finaldata[mcs].append((dataset[mcs]).get(trial,0))
    #print finaldata
    num_plots = 16

    # Have a look at the colormaps here and decide which one you'd like:
    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)])
    plt.gcf().subplots_adjust(bottom=0.15)
    leg = ['mcs '+str(i) for i in range(0,16)]
    for y in range(0,16):		
        plt.plot(finaldata[y])
        #plt.annotate('MCS' + str(y), xy=(y%9, finaldata[y][1]),fontsize=10)
    plt.suptitle(x , fontsize=15)
    plt.legend(leg,shadow=True, fancybox=True, loc = 'upper center', bbox_to_anchor=(0.5, -0.05), ncol = 10, fontsize = 5)
    plt.xlabel("Trial No")
    plt.ylabel("Delivery Ratio")
    plt.ylim([0,1])
    plt.savefig(pp, format='pdf', bbox_inches = 'tight')
    plt.clf()
    print 'done'
pp.close()    


