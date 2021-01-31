import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import math
from statistics import mean

filelist = ['1.xls', '2.xls', '3.xls', '4.xls', '5.xls', '6.xls']
for fi in filelist:
    data = pd.read_excel(fi, index_col = None)
    data['DrainI'] = abs(data['DrainI'])
    data = data.loc[:, ~np.array([False, False, False, False, False, False, False, False, True])]
    data['DrainI'][np.argmin(data['GateV'])]
    for x in range(len(data['DrainI'])):
        data['DrainI'][x] = math.sqrt(abs(data['DrainI'][x]))
    gatelist = []
    drainlist = []
    #gate is first (x), then the drain (y)
    for i in range(len(data['GateV'])):
        if data['GateV'][i] < -9.9:
            gatelist.append(data['GateV'][i])
            drainlist.append(data['DrainI'][i])
        if data['GateV'][i] < -30.01:
            break

    def best_fit_slope_and_intercept(xs,ys):
        m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
            ((mean(xs)*mean(xs)) - mean(xs*xs)))
        
        b = mean(ys) - m*mean(xs)
        
        return m, b

    m, b = best_fit_slope_and_intercept(np.array(gatelist), np.array(drainlist))

    regression_line = [(m*x)+b for x in gatelist]

    plt.scatter(data['GateV'],data['DrainI'])
    plt.plot(gatelist, regression_line, color='red')
    plt.show()

    print('The value of m in point slope form is ', m, 'the value of b is ', b)