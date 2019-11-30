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
    
def isSelected(iFileName,iMeasName,xrange,yrange,iDevice) :
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
        and devName == iDevice:
            return True, xpos, ypos
    return False, 0, 0
                
def plotMap(iDirPath,iMeasName, xrange, yrange, iDevice):
    listX = []
    listY = []
    listVnom = []
    listRnom = []
    listIdeal = []
    listPhiB = []
    for fileName in os.listdir(iDirPath): 
        res, xpos, ypos = isSelected(fileName,iMeasName,xrange,yrange,iDevice)
        if res:
            dataArray = np.genfromtxt(iDirPath + "/" + fileName,
                                      delimiter=' ',
                                      skip_header = 0)
            lVnom = getVnom(dataArray[:,0],dataArray[:,1])
            lRnom = getRnom(dataArray[:,0],dataArray[:,1])
            lIdeal, lPhiB = getBarrier(dataArray[:,0],dataArray[:,1],0.01)
            listX.append(xpos)
            listY.append(ypos)
            listVnom.append(lVnom)
            listRnom.append(lRnom)
            listIdeal.append(lIdeal)
            listPhiB.append(lPhiB)
    minX = min(listX)
    minY = min(listY)
    maxX = max(listX)
    maxY = max(listY)
    mapVnom = np.full((maxX-minX+1,maxY-minY+1), np.nan)
    mapRnom = np.full((maxX-minX+1,maxY-minY+1), np.nan)
    mapIdeal = np.full((maxX-minX+1,maxY-minY+1), np.nan)
    mapPhyB = np.full((maxX-minX+1,maxY-minY+1), np.nan)
    print("limits : %d %d %d %d" %(minX,maxX,minY,maxY))
    for i in range(len(listX)):
        mapVnom[listX[i]-minX,listY[i]-minY] = listVnom[i]
        mapRnom[listX[i]-minX,listY[i]-minY] = listRnom[i]
        mapIdeal[listX[i]-minX,listY[i]-minY] = listIdeal[i]
        mapPhyB[listX[i]-minX,listY[i]-minY] = listPhiB[i]
    
    fig, axs = plt.subplots(2,2, figsize=(10, 10),
                             constrained_layout=True)
    selected_cmpa='hot'
    fig.suptitle(iDevice+" statistics")
    axs[0,0].set_title("Vnom Map")
    im = axs[0,0].imshow(mapVnom, vmin=1.06,vmax=1.14,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=axs[0,0])
    axs[0,1].set_title("Rnom Map")
    im = axs[0,1].imshow(mapRnom, vmin=2.1,vmax=2.6,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=axs[0,1])
    axs[1,0].set_title("Ideal Factor Map")
    im = axs[1,0].imshow(mapIdeal, vmin=0.95,vmax=1.05,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=axs[1,0])
    axs[1,1].set_title("Barrier Height Map")
    im = axs[1,1].imshow(mapPhyB, vmin=1.4793,vmax=1.47945,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=axs[1,1])
    
plotMap("C:/Users/Maxime/Documents/Python Scripts/testData",
     "IVDirect",range(-100,100),range(-100,100),"D01")