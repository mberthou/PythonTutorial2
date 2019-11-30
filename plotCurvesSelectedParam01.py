# -*- coding: utf-8 -*-

import os, re
import numpy as np
import matplotlib.pyplot as plt


def getVnom(data_Va,data_Ia) :
    above_100mA = ( data_Ia > 0.01 )
    if np.any(above_100mA) :
        thresPos = np.where(above_100mA)
        return data_Va[thresPos[0][0]]
    else : return -1
    
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


def plotCurves(iDirPath,iMeasName,xrange,yrange,devList,iVnomMax):
    for fileName in os.listdir(iDirPath): 
        if isSelected(fileName,iMeasName,xrange,yrange,devList):
            dataArray = np.genfromtxt(iDirPath + "/" + fileName,
                                      delimiter=' ',
                                      skip_header = 0)
            lVnom = getVnom(dataArray[:,0],dataArray[:,1])
            
            print("Vnom :" + str(lVnom) + " V")
            if lVnom < iVnomMax :
                print("=> plot")
                plt.plot(dataArray[:,0],dataArray[:,1])
            
plotCurves("C:/Users/Maxime/Documents/Python Scripts/testData",
     "IVDirect",range(2,7),range(2,7),["D01"],1.1)