import pandas as pd
#find the highest correlative data
corel = pd.DataFrame.from_dict(features)
corel.corr(method='kendall')