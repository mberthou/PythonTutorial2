# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:22:46 2019

@author: Maxime
"""

# import os, csv
import numpy as np
from random import gauss
# from random import random
from random import seed
from datetime import datetime


def generateDiodeIV(nfact,barrier,Rser):
    temp = 300
    qelec = 1.6e-19
    kboltz = 1.380649e-23
    nktq = (nfact*kboltz*temp)/qelec
    Is = 1e-15
    Iarray = np.logspace(-15,-1,101)
    Varray = Rser*Iarray + np.log(Iarray-Is)*nktq+barrier
    Varray[0] = 0
    return Iarray,Varray


def generateDiodeFiles(targetDir):
    seed(datetime.now())
    
    for x in range(10) :
        for y in range(10) :
            for dev in ["D01","D02","D03"] :
                measName = "IVDirect"
                fileName = "20191022_X" + str(x) + "Y" + str(y)\
                    + "_" + dev + "_" + measName + ".csv"
                print( fileName )
                # file = open("testData/" + fileName,'w')
                gaussVar = gauss(1.0,0.01)
                nfact = 1.02*gaussVar
                phiBar = gaussVar*1.2
                varRon = gauss(2.0,0.1)
                xarray,yarray = generateDiodeIV(nfact, phiBar, varRon)
                varray = np.zeros((xarray.size,2))
                varray[:,1] = xarray
                varray[:,0] = yarray
                np.savetxt(targetDir + "/" + fileName, varray)
                # file.close()
                    
generateDiodeFiles("C:/Users/Maxime/Documents/Python Scripts/testData/")