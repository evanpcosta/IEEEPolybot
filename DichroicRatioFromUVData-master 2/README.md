# DichroicRatioFromUVData

After downloading the files from this repository install the dependancies using the command

```pip install -r requirements.txt```

(Best to do this in a conda environment)

In dataparser.ipynb change the directory from 

```data = pd.read_csv("/Users/evancosta/Desktop/DataParse2/12-13.csv")```

to wherever the csv file is in your computer 

Also, in the last line of dataparser.ipynb change

```dataframe = pd.read_excel('uv-vis.xlsx')```

and 

```dataframe.to_excel(r'/Users/evancosta/Desktop/DataParse2/uv-vis.xlsx', sheet_name='Your sheet name', index = False)```

to the file and directory of the file you want to write to.

