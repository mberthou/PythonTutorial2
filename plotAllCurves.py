# -*- coding: utf-8 -*-

import os, re
import numpy as np
import matplotlib.pyplot as plt

dirPath = "C:/Users/Maxime/Documents/Python Scripts/testData"
patStr = "([0-9]+)_X([-0-9]+)Y([-0-9]+)_([0-9A-Za-z]+)_([0-9A-Za-z]+).csv"
fileNamePatternCompiled = re.compile(patStr)
for fileName in os.listdir(dirPath):
    matchObj = fileNamePatternCompiled.match(fileName)
    if matchObj and matchObj.group(5) == "IVDirect" :
        dataArray = np.genfromtxt(dirPath + "/" + fileName, delimiter=' ',
                                  skip_header = 0)
        plt.plot(dataArray[:,0],dataArray[:,1])