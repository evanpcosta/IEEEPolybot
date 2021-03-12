import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

def dichroic_pre(filepath):
    data = pd.read_csv(filepath)
    data = data.dropna(axis=1, how='all')
    #print(data.shape)

    index = []
    for x in data.columns:
        if 'Unnamed' in x:
           continue
        else:
            index.append('alpha')
            index.append(x)

    data.columns = index

    data = data.loc[:,~data.columns.duplicated()]
    data = data.drop(data.index[0])
    cols = data.columns
    #print(cols)
    datarr = data.to_numpy(dtype=float)
    #print(datarr.shape)

    change = 0
    for i in range(1, len(datarr[0, :])):
        doublecheck = 0
        while doublecheck < 2:
            for x in range(len(datarr[:, i])-1):
                if change != 0:
                    datarr[x][i] += change
                else:
                    difference = datarr[x][i] - datarr[x+1][i]
                    if abs(difference) > 0.025:
                        change = difference
            change = 0
            doublecheck += 1

    #print(data.head())

    dellist = []
    for i in range(4, len(datarr[0, :])):
        if '-0' in data.columns[i]:
            datarr[:, i] -= datarr[:, 2]
        elif '-90' in data.columns[i]:
            datarr[:, i] -= datarr[:, 3]
        elif data.columns[i] == '10-2–0':
            datarr[:, i] -= datarr[:, 2]
        elif data.columns[i] == '10-2–90':
            datarr[:, i] -= datarr[:, 3]
        else:
            dellist.append(data.columns[i])

    for x in dellist:
        count = 0
        for i in data.columns:
            if i == x:
                break
            count += 1
        datarr = np.delete(datarr, count, 1)
        data = data.drop(x, axis=1)

    # remove the last row
    datarr = datarr[:-1, :]

    # make the minimum zero
    for i in range(1, len(datarr[0, :])):
        change = -min(datarr[:, i])
        for x in range(len(datarr[:, i]) - 1):
            datarr[x][i] += change
    datarr = datarr[:-1, :]
    #print(data.columns)

    seen = set()
    ratio_names = []
    ratios = []

    for col in data.columns:
        # somehow using endash with ord = 8211. Can be causing some errors
        split = re.split("-|–", col)
        if len(split) <= 1:
            continue
        else:
            sample = "-".join(split[:-1])
            if sample in seen:
                continue
            # print("Col:",col,"Split:", split," Sample: ",sample)
            ratio = -1
            try:
                seen.add(sample)
                ratio = max(datarr[:, data.columns.get_loc(sample+'-90')])/max(datarr[:, data.columns.get_loc(sample+'-0')])
                ratios.append(ratio)
                ratio_names.append(sample)
            except:
                pass
    ratio_names = np.asarray(ratio_names); ratios = np.asarray(ratios)

    return ratio_names, ratios


    # ratio2 = ninety2/zero2
    #
    # dataframe = pd.read_excel('uv-vis.xlsx')
    #
    # if 'ratio' not in dataframe.columns:
    #     dataframe.insert(len(dataframe.columns), "ratio", [None]*len(dataframe), True)
    #
    # dataframe.loc[12, 'ratio'] = ratio
    # dataframe.loc[13, 'ratio'] = ratio2
    #
    # #change the directory to the directory of the file you want to write to
    # dataframe.to_excel(r'/Users/evancosta/Desktop/DataParse2/uv-vis.xlsx', sheet_name='Your sheet name', index = False)

    # preprocess data, get an int, put it in in exact spot where it is supposed to go