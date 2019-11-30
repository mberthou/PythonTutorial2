# -*- coding: utf-8 -*-

import os, re
import numpy as np
import matplotlib.pyplot as plt
    
def getRnom(data_Va, data_Ia):
    pos_data = ( data_Ia >= 0.05 ) & ( data_Ia <= 1 )
    if np.any(pos_data):
        p = np.polyfit(data_Va[pos_data],data_Ia[pos_data], 1 )
        return 1/p[0]
    else : return -1
    
def isSelected(iFileName,iMeasName,iDevice) :
    patStr = "([0-9]+)_X([-0-9]+)Y([-0-9]+)_([0-9A-Za-z]+)_([0-9A-Za-z]+).csv"
    fileNamePatternCompiled = re.compile(patStr)
    matchObj = fileNamePatternCompiled.match(iFileName)
    if matchObj :
        xpos = int(matchObj.group(2))
        ypos = int(matchObj.group(3))
        devName = matchObj.group(4)
        measName = matchObj.group(5)
        if measName == iMeasName\
        and devName == iDevice:
            return True, xpos, ypos
    return False, 0, 0
                
def plotMap(iDirPath,iMeasName, iDevice):
    listX = []
    listY = []
    listRnom = []
    for fileName in os.listdir(iDirPath): 
        res, xpos, ypos = isSelected(fileName,iMeasName,iDevice)
        if res:
            dataArray = np.genfromtxt(iDirPath + "/" + fileName,
                                      delimiter=' ',
                                      skip_header = 0)
            lRnom = getRnom(dataArray[:,0],dataArray[:,1])
            listX.append(xpos)
            listY.append(ypos)
            listRnom.append(lRnom)
    minX = min(listX)
    minY = min(listY)
    maxX = max(listX)
    maxY = max(listY)
    mapRnom = np.full((maxX-minX+1,maxY-minY+1), np.nan)
    for i in range(len(listX)):
        mapRnom[listX[i]-minX,listY[i]-minY] = listRnom[i]
    plt.title("Rnom Map")
    im = plt.imshow(mapRnom, vmin=2.1,vmax=2.6,
               origin='upper',cmap='hot',
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    plt.colorbar(im)
    
plotMap("C:/Users/Maxime/Documents/Python Scripts/testData",
     "IVDirect","D01")