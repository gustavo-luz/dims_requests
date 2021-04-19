import json
import requests
import pandas as pd


url = "http://uiot-dims.herokuapp.com/list/data"

r = requests.get(url)


content = r.json()
#CREATE DF
df = pd.DataFrame.from_dict(content)

# some df observations
#print(df.head)
#df.info()
#print(df.describe())


# TODO add more devices according to chipset
# TODO create link between chipset and device (chipset x = id y)

# CREATE dataframe matheus - CURRENT DEVICE 
dfmath = df[df["chipset"]== "AE:08:62:24:F9:71"]
#print(dfmath.head())

# select last 2 rows (before that the sendings wasn't aggregated)
dfmath = dfmath.iloc[0:2,:]
print(dfmath)
#print(type(dfmath))


#TODO split values into columns

"""
#OPTION 1

dfmath = dfmath.str.split(expand=True,)
print(dfmath)
# AttributeError: 'DataFrame' object has no attribute 'str'
"""

"""
#OPTION 2

#convert to series
dfmath = pd.Series(dfmath.value.values.flatten())
print(dfmath)
print(type(dfmath))

dfmath = dfmath.str.split("/", expand=True)
print(dfmath)

#nan value
"""

#EXPORTING TO CSV 
# no unziping
dfmath.to_csv('out.csv',index=False) 

# if you want to zip it
"""
compression_opts = dict(method='zip',archive_name='out.csv')
dfmath.to_csv('out.zip', index=False,compression=compression_opts)  
"""


#TODO export to google sheets

