import json
import requests
import pandas as pd

class Date:
    def __init__(self, date):
        d = date.split('/')
        self.day = int(d[0])
        self.month = int(d[1])
        self.year = int(d[2]) + 2000
        self.date = date
        
class Time:
    def __init__(self, time):
        t = time.split(':')
        self.hour = int(t[0])
        self.minute = int(t[1])
        self.second = int(t[2])
        self.time = time
        self.timeInSeconds = (self.hour * 3600) + (self.minute*60) + self.second
        
class Info:                                                
    TOTAL_DISTANCE = 10.0 # Define value of TOTAL_DISTANCE constant based on container's total distance
                                                           
                                                            # Class Info constains information in column "value"
                                                            # Parameters:
    def __init__(self, info):                               #   Info.distance    -> Trash distance to the top
        instancy = info[0].split(",")                       #   Info.capacity    -> Fill percentage
                                                            #   Info.battery     -> Battery percentage
                                                            #
        self.distance = float(instancy[0])                  #   Info.time.hour   -> hour of recorded time 
        self.capacity = self.distance / self.TOTAL_DISTANCE #   Info.time.minute -> minute of recorded time 
                                                            #   Info.time.second -> second of recorded time  
        self.battery = int(instancy[1])                     #   Info.time.time   -> Original "time" string
        self.date = Date(instancy[2])                       #   Info.time.timeInSeconds -> Total time in seconds
        self.time = Time(instancy[3])                       #   
                                                            #   Info.date.day    -> day of recorded time
                                                            #   Info.date.month  -> month of recorded time
                                                            #   Info.date.year   -> year of recorded time
                                                            #   Info.date.date   -> Original "date" string


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
dfmath = df[df["chipset"] == "AE:08:62:24:F9:71"]
#print(dfmath.head())

# Acquisitions outside this range are in a wrong format
dfmath = dfmath.iloc[10:13]
print(dfmath)

# This lines splits values into columns
value = dfmath['value'].array

# For each acquisition (This one takes 10th, 11th and 12th acquisitions) an Info object is created cointaining information in "value" column
for i in value:
    print(i)
    info = Info(i)
    print(info.battery)


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
