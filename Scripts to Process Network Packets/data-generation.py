#!/usr/bin/env python
import sys, string
import re
import os,glob
import csv
from collections import OrderedDict
from subprocess import CalledProcessError, check_output


def getOrderedDataValues(dataval):
	datalist = []
	for dataobj in dataExcelList:
		datalist.append(dataval[dataobj])
	return datalist
def getOrderedRssiValues(rssival):
	rssilist = []
	for rssiobj in rssiExcelList:
		rssilist.append(rssival[rssiobj])
	return rssilist	
def isGoodLink(link):
    '''if(link == '122-118' or link == '118-122' or link == '106-116' or link == '116-106'
       or link == '122-107' or link == '122-103' or link == '121-103' or link == '106-109'
        or link == '103-121' or link == '103-122' or link == '116-108'):
		return False
    else:
		return True'''
    if(str(link).__contains__('108-116') or link.__contains__('105-109') or link.__contains__('109-105')):
        return False
    else:
        return True
    #return True
    '''del link["105-118"]
	del link["106-114"]
	del link["111-115"]
	del link["112-103"]
	del link["105-107"]'''

#Format for graph scripts
#['"Tx retry"', '"Destination"', '"Number"', '"Tx Success"', '"Source"', '"MCS"', '"Delivery Ratio"', '"Link"\n']  
dataExcel = OrderedDict({'Tx Retry':'Tx Retry','Destination':'Destination','Number':'Number','Tx Success':'Tx Success','Source':'Source','MCS':'MCS', 'Delivery Ratio':'Delivery Ratio', 'Link' : 'Link'})
dataExcelList = ['Tx Retry', 'Destination', 'Number', 'Tx Success', 'Source', 'MCS', 'Delivery Ratio', 'Link']
#RSSI-C	RSSI-A	RSSI-B	Destination	Number	Source	MCS	Mean Rssi	Delivery Ratio
rssiExcel = OrderedDict({'RSSI-C':'RSSI-C','RSSI-A':'RSSI-A','RSSI-B':'RSSI-B','Destination':'Destination','Number':'Number','Source':'Source','MCS':'MCS', 'Mean Rssi': 'Mean Rssi', 'Delivery Ratio':'Delivery Ratio', 'Link':'Link'})
rssiExcelList = ['RSSI-C','RSSI-A','RSSI-B','Destination','Number','Source','MCS','Mean Rssi','Delivery Ratio', 'Link']
#snrExcel =  {'Source':'Source','Destination':'Destination','MCS':'MCS','Number':'Number','SNR-A':'SNR-A','SNR-B':'SNR-B'}
outData = csv.writer(open('datafile.csv',"w"), delimiter=',',lineterminator='\n')
outRssi = csv.writer(open('rssi.csv',"w"), delimiter=',',lineterminator='\n')
#outSnr = csv.writer(open("snr.csv","w"), delimiter=',',lineterminator='\n')

outData.writerow(dataExcelList)
outRssi.writerow(rssiExcelList)
rootdir = '../new-data-v1/'
#outSnr.writerow(snrExcel.values())
for dirname in glob.glob(rootdir +'*'):
    #print 'dirname is', dirname
    for nodename in glob.glob(dirname +'/mcs*'):
        #print 'nodename is', nodename
        for filename in glob.glob(nodename + '/stat_send_*_*.txt'):
            #print 'filename is', filename
            file = open (filename, 'r')
            lines = file.readlines()
            file.close()
            #snrValues = {'Source':'','Destination':'','MCS':'','Number':'','SNR-A':0,'SNR-B':0}
            filename = filename.replace('.txt', '')
            fileValues = string.split(filename,'_')
            if(isGoodLink(fileValues[2]+'-'+fileValues[3]) == False):
                continue;
            dataValues = {'Tx Retry':0,'Destination':'','Number':'','Tx Success':0,'Source':'','MCS':'', 'Delivery Ratio':0, 'Link' : ''}
            rssiValues = {'RSSI-C':0,'RSSI-A':0,'RSSI-B':0,'Destination':'','Number':0,'Source':'','MCS':'', 'Mean Rssi': 0, 'Delivery Ratio':0, 'Link':''}
            dataValues['Source'] = fileValues[2]
            dataValues['Destination'] = fileValues[3]
            dataValues['MCS'] = nodename.replace(dirname + '/', '')
            #dataValues['Number'] = re.search(r'\d+',fileValues[4]).group()
            dataValues['Link'] = fileValues[2] + '-' + fileValues[3]
            dataValues['Number'] = 1

            rssiValues['Source'] = fileValues[2]
            rssiValues['Destination'] = fileValues[3]
            rssiValues['MCS'] = nodename.replace(dirname + '/', '')
            #rssiValues['Number'] = re.search(r'\d+',fileValues[4]).group()
            rssiValues['Link'] = fileValues[2] + '-' + fileValues[3]
            rssiValues['Number'] = 1

            #snrValues['Source'] = fileValues[2]
            #snrValues['Destination'] = fileValues[3]
            #snrValues['MCS'] = dirname
            #snrValues['Number'] = re.search(r'\d+',fileValues[4]).group()
            txSuccess = ''
            #sys_call = 'wc -l '+ rootdir + dataValues['Destination'] + '/' + dataValues['MCS'] + '/'  +'recv' + dataValues['Source'] + '_' + dataValues['Number']+'.txt'
            #print sys_call
            sys_call = 'wc -l '+ rootdir + dataValues['Destination'] + '/' + dataValues['MCS'] + '/'  +'recv' + dataValues['Source'] +'_1.txt'
            try :
                retVal = check_output(sys_call, shell=True)
            except CalledProcessError as e:          
                print e.returncode
                retVal = '0 0'                     
            dataValues['Tx Success'] = float(retVal.split(' ')[0])
            iterator = 0
            while (iterator < len(lines)):
               line = lines[iterator]
               for key in dataExcel:
                   if(re.search(key,line,re.IGNORECASE) > 0 and key !='Source' and str(key).lower() != 'tx success'):
                        val = re.search(r'\d+',line).group()
                        dataValues[key] = val
                        #print val
                        break
                   elif(re.search(key,line,re.IGNORECASE) > 0 and key !='Source'):
                        if (dataValues['MCS'].__contains__('mcs0')) and (dataValues['Link'].__contains__('103-107') or dataValues['Link'].__contains__('107-122') or dataValues['Link'].__contains__('107-118')):
                            print dataValues                  
                            val = re.search(r'\d+',line).group()                          
                            dataValues[key] = val
                            print val
                            break                                   
               for keyrssi in rssiExcel:
                   if(re.search(keyrssi,line,re.IGNORECASE) > 0 and key !='Source'):
                        val = re.search(r'\d+',line).group()
                        rssiValues[keyrssi] = val
                        #print val
                        break
                   elif(re.search(key,line,re.IGNORECASE) > 0 and key !='Source'):
                        if (dataValues['MCS'].__contains__('mcs0')) and (dataValues['Link'].__contains__('103-107') or dataValues['Link'].__contains__('107-122') or dataValues['Link'].__contains__('107-118')):
                            print dataValues                  
                            val = re.search(r'\d+',line).group()                           
                            dataValues[key] = val
                            print val
                            break  
               #for keysnr in snrExcel:
                   #if(re.search(keysnr,line,re.IGNORECASE) > 0 and key!='Source'):
                        #val = re.search(r'\d+',line).group()
                        #snrValues[keysnr] = val
                        #break
               iterator = iterator + 1
            rssiValues['Mean Rssi'] = (int(rssiValues['RSSI-A']) + int(rssiValues['RSSI-B']) + int(rssiValues['RSSI-C']))/3                
            deliveryRatio = 0.0
            #print dataValues['Tx Success']
            if(int(dataValues['Tx Success']) > 1200):
                deliveryRatio = float(1200 / (1200 + float(dataValues['Tx Retry'])))
            else:
                deliveryRatio = float(float(dataValues['Tx Success']) /  1200)
            #print deliveryRatio
            rssiValues['Delivery Ratio'] = deliveryRatio
            dataValues['Delivery Ratio']  = deliveryRatio
            outData.writerow(getOrderedDataValues(dataValues))
            outRssi.writerow(getOrderedRssiValues(rssiValues))
            #outSnr.writerow(snrValues.values())
