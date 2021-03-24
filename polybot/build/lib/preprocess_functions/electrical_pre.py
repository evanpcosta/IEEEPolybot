import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from statistics import mean

def electrical_pre(fi):
    data = pd.read_excel(fi, index_col=None)
    data['DrainI'] = abs(data['DrainI'])
    data = data.loc[:, ~np.array([False, False, False, False, False, False, False, False, True])]
    data['DrainI'][np.argmin(data['GateV'])]
    data["DrainI"] = np.sqrt(data["DrainI"].abs())
    gatelist = []
    drainlist = []
    # gate is first (x), then the drain (y)
    for i in range(len(data['GateV'])):
        if data['GateV'][i] < -9.9:
            gatelist.append(data['GateV'][i])
            drainlist.append(data['DrainI'][i])
        if data['GateV'][i] < -30.01:
            break

    def best_fit_slope_and_intercept(xs, ys):
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
             ((mean(xs) * mean(xs)) - mean(xs * xs)))

        b = mean(ys) - m * mean(xs)

        return m, b

    m, b = best_fit_slope_and_intercept(np.array(gatelist), np.array(drainlist))

    return m, b