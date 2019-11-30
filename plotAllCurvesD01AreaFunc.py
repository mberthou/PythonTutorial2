# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:49:21 2019

@author: Maxime
"""


import os, re
import numpy as np
import matplotlib.pyplot as plt
    
def isSelected(iFileName,xrange,yrange,devs) :
    patStr = "([0-9]+)_X([-0-9]+)Y([-0-9]+)_([0-9A-Za-z]+)_([0-9A-Za-z]+).csv"
    fileNamePatternCompiled = re.compile(patStr)
    matchObj = fileNamePatternCompiled.match(iFileName)
    if matchObj :
        xpos = int(matchObj.group(2))
        ypos = int(matchObj.group(3))
        devName = matchObj.group(4)
        measName = matchObj.group(5)
        if measName == "IVDirect"\
        and xpos in xrange\
        and ypos in yrange\
        and devName in devs:
            print(devName+" X"+str(xpos)+"Y"+str(ypos))
            return True
    return False


def plotCurves(iDirPath,xrange,yrange,devs):
    for fileName in os.listdir(iDirPath): 
        if isSelected(fileName,xrange,yrange,devs):
            dataArray = np.genfromtxt(iDirPath + "/" + fileName,
                                      delimiter=' ',
                                      skip_header = 0)
            plt.plot(dataArray[:,0],dataArray[:,1])
            
plotCurves("C:/Users/Maxime/Documents/Python Scripts/testData",
     range(3,7),range(3,7),["D01"])