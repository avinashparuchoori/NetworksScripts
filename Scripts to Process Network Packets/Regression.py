__author__ = 'avinash'
from numpy import array,linalg, ones,vstack, random
import numpy as np
import string

class LinregNumpy():
    """
    Use numpy to solve a multivariate linear regression
    """
    def train(self,X,y):
        """
        X - input list of lists
        y - input column vector in list form, ie [[1],[2]]
        """
        assert len(y) == len(X)
        X = vstack([array(X).T,ones(len(X))]).T
        self.coefs = linalg.lstsq(X,y)[0]
        self.coefs = self.coefs.reshape(self.coefs.shape[0],-1)

    def predict(self,Z):
        """
        Z - input list of lists
        """
        Z = vstack([array(Z).T,ones(len(Z))]).T
        return Z.dot(self.coefs)
    def transpose(self, X):
        """
        Transpose the matrix in place.
        """
        trans = []
        for j in xrange(0, len(X[0])):
            row = []
            for i in xrange(0,len(X)):
                row.append(X[i][j])
            trans.append(row)
        X = trans
        return X

datafile = open('../latest/datafile.csv', 'r')
lines = datafile.readlines()
datafile.close()

trainX = []
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
trainX = MCS[0:8]
trainY = MCS[8:16]
datafile = open('datafile.csv', 'r')
lines = datafile.readlines()
datafile.close()

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
predictX = MCS[0:8]
predictY = MCS[8:16]
for i in xrange(0, 8, 1):
    lr = LinregNumpy()
    lr.train(lr.transpose(trainX), trainY[i])
    T =  (lr.predict(lr.transpose(predictX)))
    data = [predictY[i], T]
    data = lr.transpose(data)
    np.savetxt('predictions/coeffs_for_mcs'+ str(i + 8)+'.csv', lr.coefs, delimiter=',')
    np.savetxt('predictions/mcs'+ str(i + 8)+'.csv', data, delimiter=',')
    sum = 0
    for j in range(0 , len(predictY[i]), 1):
        sum = sum + np.square(predictY[i][j] - T[i])
    print np.sqrt(sum)/len(predictY[i])