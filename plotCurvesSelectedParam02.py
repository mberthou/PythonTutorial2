# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:20:20 2019

@author: Maxime
"""

import os, re
import numpy as np
import matplotlib.pyplot as plt


def getVnom(data_Va,data_Ia) :
    above_100mA = ( data_Ia > 0.01 )
    if np.any(above_100mA) :
        thresPos = np.where(above_100mA)
        return data_Va[thresPos[0][0]]
    else : return -1
    
def getRnom(data_Va, data_Ia):
    pos_data = ( data_Ia >= 0.05 ) & ( data_Ia <= 1 )
    if np.any(pos_data):
        p = np.polyfit(data_Va[pos_data],data_Ia[pos_data], 1 )
        return 1/p[0]
    else : return -1
    
def getBarrier(data_Va, data_Ia,iArea):
    n = 0
    phi = 0
    richard = 146
    lTemp = 300
    kbTq = 8.617e-5*lTemp
    selV = data_Va[(data_Ia > 1e-7) & (data_Ia < 1e-5)]
    selI = data_Ia[(data_Ia > 1e-7) & (data_Ia < 1e-5)]
    if len(selI) >= 4:
        lnIk = np.log(selI/(lTemp*lTemp*richard*iArea))
        lnIk = lnIk*kbTq
        a,b = np.polyfit(selV,lnIk,1)
        n = 1/a
        phi = -1*b
    return n,phi
    
def isSelected(iFileName,iMeasName,xrange,yrange,devList) :
    patStr = "([0-9]+)_X([-0-9]+)Y([-0-9]+)_([0-9A-Za-z]+)_([0-9A-Za-z]+).csv"
    fileNamePatternCompiled = re.compile(patStr)
    matchObj = fileNamePatternCompiled.match(iFileName)
    if matchObj :
        xpos = int(matchObj.group(2))
        ypos = int(matchObj.group(3))
        devName = matchObj.group(4)
        measName = matchObj.group(5)
        if measName == iMeasName\
        and xpos in xrange\
        and ypos in yrange\
        and devName in devList:
            print("\nD01 X"+str(xpos)+"Y"+str(ypos))
            return True
    return False


def plotCurves(iDirPath,iMeasName,xrange,yrange,devList,iVnomMax,iRnomMax):
    for fileName in os.listdir(iDirPath): 
        if isSelected(fileName,iMeasName,xrange,yrange,devList):
            dataArray = np.genfromtxt(iDirPath + "/" + fileName,
                                      delimiter=' ',
                                      skip_header = 0)
            lVnom = getVnom(dataArray[:,0],dataArray[:,1])
            lRnom = getRnom(dataArray[:,0],dataArray[:,1])
            lIdeal, lPhi = getBarrier(dataArray[:,0],dataArray[:,1],0.01)
            
            print("Vnom :" + str(lVnom) + " V")
            print("Rnom :" + str(lRnom) + " V")
            print("Ideality :" + str(lIdeal))
            print("PhiB :" + str(lPhi) + " eV")
            if lVnom < iVnomMax and lRnom < iRnomMax and lIdeal < 1.02:
                print("=> plot")
                plt.plot(dataArray[:,0],dataArray[:,1])
            
plotCurves("C:/Users/Maxime/Documents/Python Scripts/testData",
     "IVDirect",range(2,7),range(2,7),["D01"],1.1,2.2)