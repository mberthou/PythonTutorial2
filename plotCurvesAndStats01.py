# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:20:51 2019

@author: Maxime
"""


import os, re
import numpy as np
import matplotlib.pyplot as plt

def getVt(data_Va,data_Ia):
    above_1uA = ( data_Ia > 1e-6 )
    if np.any(above_1uA) :
        thresPos = np.where(above_1uA)
        return data_Va[thresPos[0][0]]
    else : return -1
    
def getVnom(data_Va,data_Ia):
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

def prepareSimpleIVFigure():
    fig = plt.figure(figsize=(5,5))
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel("Vak (V)",fontsize=20)
    ax1.set_ylabel("Ia (A)",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ax1.grid(True)          
    # ax1.autoscale_view(False)
    ax1.set_yscale('linear')
    return ax1

def prepareDoubleIVFigure():
    fig = plt.figure(figsize=(5,2),dpi=200)
    ax1 = fig.add_subplot(121)
    ax1.set_xlabel("Vak (V)",fontsize=5)
    ax1.set_ylabel("Ia (A)",fontsize=5)
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    ax1.grid(True)          
    ax1.autoscale_view(True)
    ax1.set_yscale('linear')
    
    ax2 = fig.add_subplot(122)
    ax2.set_xlabel("Vak (V)",fontsize=5)
    ax2.set_ylabel("Ia (A)",fontsize=5)
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    ax2.grid(True)          
    # ax2.autoscale_view(True)
    ax2.set_yscale('log')
    fig.tight_layout()
    return ax1, ax2
    
def addCurve(axis,dataX,dataY):
   return axis.plot(dataX,dataY) #,'ro-')

def setQtGui():
    try:
        import IPython
        shell = IPython.get_ipython()
        shell.enable_matplotlib(gui='qt')
    except:
        pass

def plotAllIVCurvesIn(dirPath):   
    patStr = "([0-9]+)_X([-0-9]+)Y([-0-9]+)_([0-9A-Za-z]+)_([0-9A-Za-z]+).csv"
    # datePos =1
    # xCoordPos = 2
    # yCoordPos = 3
    # devNamePos = 4
    measNamePos = 5

    setQtGui()
    axis1,axis2 = prepareDoubleIVFigure()
    fileNamePatternCompiled = re.compile(patStr)
    lVtList = []
    lVnomList = []
    for fileName in os.listdir(dirPath):
        # print( fileName )
        matchObj = fileNamePatternCompiled.match(fileName)
        if matchObj:
            measName = matchObj.group(measNamePos)
            
            if measName == "IVDirect":
                dataArray = np.genfromtxt(dirPath + "/" + fileName, delimiter=' ',
                                      skip_header = 0)
                data_Va = dataArray[:,0]
                data_Ia = dataArray[:,1]
                lVt = getVt(data_Va,data_Ia)
                lVtList.append(lVt)
                lVnom = getVnom(data_Va,data_Ia)
                lVnomList.append(lVnom)
                lRnom = getRnom(data_Va,data_Ia)
                if (lVt > 0.5 and lVnom > 0 and lVnom < 2 and lRnom > 0 and lRnom < 5) :
                    addCurve(axis1,data_Va,data_Ia)
                    addCurve(axis2,data_Va,data_Ia)
                    
plotAllIVCurvesIn("C:/Users/Maxime/Documents/Python Scripts/testData")