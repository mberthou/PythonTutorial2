# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

filePath = "C:/Users/Maxime/Documents/Python Scripts/"\
            "testData/20191022_X0Y0_D03_IVDirect.csv"
dataArray = np.genfromtxt(filePath, delimiter=' ', skip_header = 0)
plt.plot(dataArray[:,0],dataArray[:,1])