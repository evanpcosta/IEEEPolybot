import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("/Users/evancosta/Desktop/DataParse2/12-13.csv") 
data = data.dropna(axis=1, how='all')

index = []
for x in data.columns:
    if 'Unnamed' in x:
       continue 
    else:
        index.append('alpha')
        index.append(x)
data.columns = index

data.columns = index

data = data.loc[:,~data.columns.duplicated()]
data = data.drop(data.index[0])
datarr = data.to_numpy(dtype=float)

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
for i in range(1, len(datarr[0, :])):
    plt.plot(datarr[:,i])

#subtract the pdms substrate 
datarr[:,4] -= datarr[:, 1]
datarr[:,5] -= datarr[:, 2]
datarr[:,6] -= datarr[:, 3]
datarr[:,7] -= datarr[:, 3]
datarr[:,8] -= datarr[:, 2]

for i in range(4, len(datarr[0, :])):
    plt.plot(datarr[:,i])

for i in range(1, len(datarr[0, :])):
    change = -datarr[0][i]
    for x in range(len(datarr[:, i])-1):
        datarr[x][i] += change
for i in range(4, len(datarr[0, :])):
    plt.plot(datarr[:,i])

#remove the last row
datarr = datarr[:-1,:]
for i in range(4, len(datarr[0, :])):
    plt.plot(datarr[:,i])

#compute ratio 
zero = max(datarr[:,5])
ninety = max(datarr[:,6])

zero2 = max(datarr[:,8])
ninety2 = max(datarr[:,7])

ratio = ninety/zero
ratio2 = ninety2/zero2
print(ratio)
print(ratio2)

plt.show()

dataframe = pd.read_excel('uv-vis.xlsx')
dataframe

if 'ratio' not in dataframe.columns:
    dataframe.insert(len(dataframe.columns), "ratio", [None]*len(dataframe), True)
dataframe

dataframe.loc[12, 'ratio'] = ratio
dataframe.loc[13, 'ratio'] = ratio2
dataframe

#change the directory to the directory of the file you want to write to 
dataframe.to_excel(r'/Users/evancosta/Desktop/DataParse2/uv-vis.xlsx', sheet_name='Your sheet name', index = False)
    
