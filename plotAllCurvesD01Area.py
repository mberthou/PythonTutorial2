import os, re
import numpy as np
import matplotlib.pyplot as plt

dirPath = "C:/Users/Maxime/Documents/Python Scripts/testData"
patStr = "([0-9]+)_X([-0-9]+)Y([-0-9]+)_([0-9A-Za-z]+)_([0-9A-Za-z]+).csv"
fileNamePatternCompiled = re.compile(patStr)
for fileName in os.listdir(dirPath):
    matchObj = fileNamePatternCompiled.match(fileName)
    if matchObj :
        xpos = int(matchObj.group(2))
        ypos = int(matchObj.group(3))
        devName = matchObj.group(4)
        measName = matchObj.group(5)
        if measName == "IVDirect"\
        and xpos in range(3,7)\
        and ypos in range(3,7)\
        and devName == "D01" :
            print(devName +" X"+str(xpos)+"Y"+str(ypos))
            dataArray = np.genfromtxt(dirPath + "/" + fileName, delimiter=' ',
                                  skip_header = 0)
            plt.plot(dataArray[:,0],dataArray[:,1])