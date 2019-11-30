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

def setQtGui():
    try:
        import IPython
        shell = IPython.get_ipython()
        shell.enable_matplotlib(gui='qt')
    except:
        pass

def plotMap(iDirPath,iMeasName, xrange, yrange, iDevice):
    listX = []
    listY = []
    listVnom = []
    listRnom = []
    listIdeal = []
    listPhiB = []
    fig, axs = plt.subplots(5,2, figsize=(10, 25),
                             constrained_layout=True)
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
            if lVnom < 1.12 and lRnom < 2.4 and lIdeal < 1.03:
                axs[0,0].plot(dataArray[:,0],dataArray[:,1])
            if lRnom > 2.5:
                axs[0,1].plot(dataArray[:,0],dataArray[:,1])
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
    
    
    selected_cmpa='hot'
    fig.suptitle(iDevice+" report")
    
    #############
    curAxis = axs[1,0]
    curAxis.set_title("Vnom Map")
    im = curAxis.imshow(mapVnom, vmin=1.06,vmax=1.14,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=curAxis)
    
    curAxis = axs[1,1]
    curAxis.hist(listVnom,bins='auto')
    curAxis.set_xlabel("Vnom (V)")
    
    #############
    curAxis = axs[2,0]
    curAxis.set_title("Rnom Map")
    im = curAxis.imshow(mapRnom, vmin=2.1,vmax=2.6,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=curAxis)
    
    curAxis = axs[2,1]
    curAxis.hist(listRnom,bins='auto')
    curAxis.set_xlabel("Rnom")
    
    #############
    curAxis = axs[3,0]
    curAxis.set_title("Ideality Factor Map")
    im = curAxis.imshow(mapIdeal, vmin=0.95,vmax=1.05,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=curAxis)
    
    curAxis = axs[3,1]
    curAxis.hist(listIdeal,bins='auto')
    curAxis.set_xlabel("Ideality")
    
    #############
    curAxis = axs[4,0]
    curAxis.set_title("Barrier Height Map")
    im = curAxis.imshow(mapPhyB, vmin=1.4793,vmax=1.47945,
               origin='upper',cmap=selected_cmpa,
               extent=([minX-0.5, maxX+0.5, maxY+0.5, minY-0.5]))
    fig.colorbar(im, ax=curAxis)
    
    curAxis = axs[4,1]
    curAxis.hist(listPhiB,bins='auto')
    curAxis.set_xlabel("PhiB (eV)")
    
setQtGui()
plotMap("C:/Users/Maxime/Documents/Python Scripts/testData",
     "IVDirect",range(-100,100),range(-100,100),"D01")