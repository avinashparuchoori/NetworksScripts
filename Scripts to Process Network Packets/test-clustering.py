__author__ = 'avinash'
import matplotlib.pyplot as plt
from math import exp
import re
import sys, string
from matplotlib.backends.backend_pdf import PdfPages
import math
import numpy as np
import scipy
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as hier
import random
from sets import Set
from collections import OrderedDict
import itertools
import csv


outfile = csv.writer(open("cluster-count.csv","w"), delimiter=',',lineterminator='\n')
#function to process the data in excel
def process(val):
    val = val.replace('"', '')
    val = val.replace('\n', '')
    return val


datafile = open('datafile.csv', 'r')
lines = datafile.readlines()
datafile.close()

pp = PdfPages('hierarchial-clustering-rssi.pdf')

link = {}
trial = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}
iterator = 1
while iterator < len(lines):
    line = lines[iterator]
    values = string.split(line, ',')
    trimmed = values[7].replace('"', '')
    trimmed = trimmed.replace('\n', '')
    link.update({trimmed: 0})
    iterator = iterator + 1
print link
print len(link)

dataset = {}  # loop through all mcs
count = 0
for lnk in link:  # loop through each link in mcs
    linkvalues = []
    for x in range(0, 16):
        mcsvalues = {}
        iterator = 1
        while (iterator < len(lines)):
            line = lines[iterator]
            values = string.split(line, ',')
            trimmedlink = values[7].replace('"', '')
            trimmedlink = trimmedlink.replace('\n', '')
            trimmedmcs = values[5].replace('"', '')
            if (trimmedlink == lnk and ('mcs' + str(x)) == trimmedmcs):  # check link and add values to list
                mcsvalues.update({int(values[2]): float(values[6])})
            iterator = iterator + 1
        # print lnkvalues
        #if len(mcsValues) == 10: #check if link has all trials
        linkVal=[]
            #for y in range(0,10):
        for obj in mcsvalues:
            linkVal.append(mcsvalues[obj])
        linkvalues.append(linkVal)
    dataset.update({lnk: linkvalues})
data = []
print 'reached after data processing '
#print len(dictmcs['mcs0'])
#print len(dictmcs['mcs0']['0'])
#print dictmcs['mcs0']['0']


#get list from the hierarchial clustering tree
def makeList( aNode):
    if aNode is None:
        # Stop recursing here
        return []
    if(aNode.is_leaf()):
        return makeList(aNode.get_left()) + [aNode.id] + makeList(aNode.get_right())
    else:
        return makeList(aNode.get_left()) + makeList(aNode.get_right())

#get all clustersets for which the distance is less than threshold
def getclusterset(T, thresh):
    clusterset = []
    if T.is_leaf():
        return None
    else:
        if(T.dist < thresh ):
            clusterset.append(T)
        leftcluster = getclusterset(T.left, thresh)
        rightcluster = getclusterset(T.right, thresh)
        if(leftcluster is not None):
            for obj in leftcluster:
                if(obj is not None):
                    clusterset.append(obj)
        if(rightcluster is not None):
            for obj in rightcluster:
                if(obj is not None):
                    clusterset.append(obj)
    return clusterset

#get the list of clusters
def getclusterlist(t):
    rssithresh = {}
    for i in np.arange(0.1, .25, 0.05):
        clusterset = []
        clusterset = getclusterset(t, i)
        rssithresh.update({i: clusterset})
    return rssithresh


linkcluster = {}
for lnk in dataset:
    datamatrix = np.array(dataset[lnk])
    #print datamatrix

    distancematrix = dist.pdist(datamatrix, 'euclidean')
    #print distancematrix

    distancematrix = distancematrix / math.sqrt(10)

    linkagematrix = hier.linkage(distancematrix, method='complete')
    #print linkagematrix

    #heatmaporder = hier.leaves_list(linkagematrix)
    t = hier.to_tree(linkagematrix, rd=False)

    cluster = {}
    #if(lnk =='102-120' or lnk == '121-103' or lnk == '105-104'):
    if(lnk == '108-116', '108-114'):
        cluster = getclusterlist(t)
        #print cluster
        linkcluster.update({lnk: cluster})

    hier.dendrogram(linkagematrix, orientation='top')
    #plt.savefig("scipy-dendrogram" + lnk + ".png")
    #plt.xlabel("mcs no")
    #plt.ylabel("distance")
    #plt.suptitle(lnk, fontsize=15)
    #plt.savefig(pp, format='pdf')
    #plt.clf()
#pp.close()

#count occurences of each cluster
def countOccurences(lst, target, thresh):
    count = 0
    for ln in lst:
        found = 0
        for obj in lst[ln][thresh]:
            if(found == 1):
                continue
            if(compareClusters(obj, target) == 0):
                count = count + 1
                found = 1
    return count

#compare if contains
def containsClusters(c1, c2):
    list1 = sorted(makeList(c1))
    list2 = sorted(makeList(c2))
    if(set(list2).issubset(set(list1))):
        return 0
    else :
        return 1
#compare two clusters
def compareClusters(c1, c2):
    list1 = sorted(makeList(c1))
    list2 = sorted(makeList(c2))
    if(set(list2).issubset(set(list1))):
        return 0
    else :
        return 1

def getuniquelist(lst):
    uniquelst = []
    for obj in lst:
        if(countOccurences(uniquelst, obj) == 0 ):
            uniquelst.append(obj)
    return uniquelst

#get clusters and counts for each threshold value in a particular range
def getClustersPerThreshold(linkcluster):
    totalclusters = {}
    for lnk in linkcluster:
        perlinkCluster = {}
        for i in np.arange(0.1, 0.25, 0.05):
            perthreshlist = {}
            biCluster = set()
            triCluster = set()
            multiCluster = []
            for obj in linkcluster[lnk][i]:
                target = sorted(makeList(obj))
                noofelements = len(target)
                if(noofelements == 2):
                    biCluster.add(str(target))
                elif(noofelements == 3):
                    bilist = [sorted(list(item)) for item in itertools.permutations(target , 2)]
                    for elem in bilist:
                        biCluster.add(str(elem))
                    triCluster.add(str(target))
                else :
                    multiCluster.append(obj)
                    bilist = [sorted(list(item)) for item in itertools.permutations(target , 2)]
                    trilist = [sorted(list(item)) for item in itertools.permutations(target , 3)]
                    for elem in bilist:
                        biCluster.add(str(elem))
                    for elem in trilist:
                        triCluster.add(str(elem))
            perthreshlist.update({2: biCluster})
            perthreshlist.update({3: triCluster})
            perthreshlist.update({4 : multiCluster})
            #print 'printing per link cluster'
            perlinkCluster.update({i : perthreshlist})
        totalclusters.update({lnk : perlinkCluster})
    clusterperthresh = {}
    doubleclusterperthresh = {}
    tripleclusterperthresh = {}
    multiclusterperthresh = {}
    for i in np.arange(0.1, 0.25, 0.05):
        dualCluster = {}
        tripleCluster = {}
        clustercount = {}
        measuredCount = set()
        for lnk in totalclusters:
            for elem in totalclusters[lnk][i][2]:
                if(dualCluster.has_key(elem)):
                    #print 'key discovered', elem, dualCluster[elem]
                    dualCluster.update({elem : dualCluster[elem] + 1})
                else:
                    #print 'no key found', elem
                    dualCluster.update({elem : 1})
            for elem in totalclusters[lnk][i][3]:
                if(tripleCluster.has_key(elem)):
                  tripleCluster.update({elem : tripleCluster[elem] + 1})
                else:
                  tripleCluster.update({elem : 1})
            for obj in totalclusters[lnk][i][4]:
                target = str(sorted(makeList(obj)))
                if(measuredCount.__contains__(target)):
                    continue
                measuredCount.add(target)
                count = countOccurences(linkcluster, obj, i)
                clustercount.update({target: count})
        #print 'dual cluster is', dualCluster
        doubleclusterperthresh.update({i : dualCluster})
        tripleclusterperthresh.update({i : tripleCluster})
        multiclusterperthresh.update({i : clustercount})
    clusterperthresh.update({2 : doubleclusterperthresh})
    clusterperthresh.update({3 : tripleclusterperthresh})
    clusterperthresh.update({4 : multiclusterperthresh})
    return clusterperthresh
#print clusterperthresh
def compareLists(l1, l2):
    if(len(l1.split(',')) != len(l2.split(','))):
        return len(l1.split(',')) - len(l2.split(','))
    list1 = [float(i) for i in l1.replace(']', '').replace('[','').split(',')]
    list2 = [float(i) for i in l2.replace(']', '').replace('[','').split(',')]
    for i in range(0, len(list1), 1):
        if(list1[i] < list2[i]):
            return -1
        elif (list1[i] > list2[i]) :
            return 1
        else :
            continue

outfile.writerow(['Group', 'Threshold', 'Count'])

clusterperthresh = getClustersPerThreshold(linkcluster)
for j in np.arange(2, 5, 1):
    for i in np.arange(0.1, 0.25, 0.05):
        for obj in clusterperthresh[j][i]:
            outfile.writerow([obj, i , clusterperthresh[j][i][obj]])

for j in np.arange(2, 5, 1):
 for i in np.arange(0.1, .25, 0.05):
    print '############################ Count for each group in ' + str(i) + ' threshold ################################'
    for obj in clusterperthresh[j][i]:
        print str(obj) + ' and count is ' + str(clusterperthresh[j][i][obj])
for j in np.arange(2, 5, 1):
 for i in np.arange(0.1, .25, 0.05):
    #print clusterperthresh[i].keys()
    width = 0.2
    fig, ax = plt.subplots()
    #print list(clusterperthresh[i].values())
    #print list(clusterperthresh[i].keys())
    #fig1 = plt.gcf()
    #fig1.set_size_inches(10, 15)
    if( j != 4):
        clusterperthresh[j][i] = OrderedDict(OrderedDict(sorted(clusterperthresh[j][i].items(), key=lambda t: t[1], reverse= True)).items()[:30])
        N = len(clusterperthresh[j][i])
    else :
        clusterperthresh[j][i] = OrderedDict(OrderedDict(sorted(clusterperthresh[j][i].items(), key=lambda t: t[1], reverse= True)).items()[:30])
        N = len(clusterperthresh[j][i])
    '''print clusterperthresh[j][i].values()'''
    ind = np.arange(N)
    print 'N is ' + str(N)
    print ind
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    rects1 = ax.barh(ind, list(clusterperthresh[j][i].values()), height = width, align = 'center', color='b', alpha = 0.2)
    ax.set_ylabel('MCS Clusters')
    ax.set_xlabel('Number of Links')
    ax.set_title('Count for group for threshold '+ str(i))
    #ax.set_yticks(ind + width)
    plt.yticks(np.arange(len(clusterperthresh[j][i].keys())),clusterperthresh[j][i].keys(), fontsize = 3)
    plt.xticks(np.arange(1, max(clusterperthresh[j][i].values())+2, 1.0), fontsize = 3)
    #ax.set_xticklabels(range(0, max(clusterperthresh[j][i].values()) + 2, 1))
    #ax.legend(clusterperthresh[i].keys())
    plt.savefig(pp, format='pdf', bbox_inches = 'tight')
    plt.clf()
pp.close()

file = open('rssi.csv','r')
lines = file.readlines()
file.close()
iterator = 1

rssiValues = [75,85,95]
#lossValues = [[]for _ in range(7)]
lossValues = {}
print 'length of rssi values ' + str(len(rssiValues))
while(iterator < len(lines)):
    line = lines[iterator]
    values = string.split(line,',')
    for x in range(0 , len(rssiValues)):
        key = rssiValues[x]
        if(x == 0):
            prev = 0
            next = float(rssiValues[x])
        elif (x == 2):
            prev = float(rssiValues[x - 1])
            next = 999999999999999
        else :
            prev = float(rssiValues[x - 1])
            next = float(rssiValues[x])
        values[9] = process(values[9])
        if ((float(values[7]) < next) and (float(values[7]) > prev)):

            if(lossValues.has_key(key)):
                klist = []
                klist.extend(lossValues[key])
                klist.append(values[9])
                lossValues.update({key: klist})
            else:
                lossValues.update({key: [values[9]]})
    iterator = iterator + 1
print 'total loss values are ' + str(len(lossValues))
for rssi in lossValues:
 rssiLinkCluster = {}
 for lnk in lossValues[rssi]:
        rssiLinkCluster.update({lnk:linkcluster[lnk]})
 clusterperthresh = {}
 clusterperthresh = getClustersPerThreshold(rssiLinkCluster)
 if(float(rssi) == 85):
    ttle = 'hierarchial-clustering-rssi ( -'+ str(rssi) + ' - -' + str(rssi - 10)+' )specific.pdf'
 else:
    ttle = 'hierarchial-clustering-rssi ( ' + ' -' + str(rssi)+' )specific.pdf'
 pp =  PdfPages(ttle)


 for j in np.arange(2, 5, 1):
    for i in np.arange(0.1, .2, 0.05):
        N = len(clusterperthresh[j][i])
        ind = np.arange(N)
        #print 'N is ' + str(N)
        #print ind
    #print clusterperthresh[i].keys()
        width = 0.05
        fig, ax = plt.subplots()
    #print list(clusterperthresh[i].values())
    #print list(clusterperthresh[i].keys())
    #fig1 = plt.gcf()
    #fig1.set_size_inches(10, 15)
        if( j != 4):
            clusterperthresh[j][i] = OrderedDict(OrderedDict(sorted(clusterperthresh[j][i].items(), key=lambda t: t[1], reverse= True)).items()[:30])
            N = len(clusterperthresh[j][i])
        else :
            clusterperthresh[j][i] = OrderedDict(OrderedDict(sorted(clusterperthresh[j][i].items(), key=lambda t: t[1], reverse= True)).items()[:30])
            N = len(clusterperthresh[j][i])
        '''print clusterperthresh[j][i].values()'''
        ind = np.arange(N)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        rects1 = ax.barh(ind, list(clusterperthresh[j][i].values()), height = width, align = 'center', color='b', alpha = 0.4)
        ax.set_ylabel('MCS Clusters')
        ax.set_xlabel('Number of Links')
        ax.set_title('Count for group for threshold '+ str(i))
        #ax.set_yticks(ind + width)
        plt.yticks(np.arange(len(clusterperthresh[j][i].keys())),clusterperthresh[j][i].keys(), fontsize = 3)
        plt.xticks(np.arange(1, max(clusterperthresh[j][i].values())+2, 1.0), fontsize = 4)
        #ax.set_xticklabels(range(0, max(clusterperthresh[j][i].values()) + 2, 1))
        #ax.legend(clusterperthresh[i].keys())
        plt.savefig(pp, format='pdf', bbox_inches = 'tight')
        plt.clf()
 pp.close()
