import json
import requests
import pandas as pd
from container import Container
       


url = "http://uiot-dims.herokuapp.com/list/data"

r = requests.get(url)


content = r.json()
# CREATE DF
df = pd.DataFrame.from_dict(content)

# TODO add more devices according to chipset
# TODO create link between chipset and device (chipset x = id y)


# Another way is to call function "dfmath = df.where(df["chipset"] == "AE:08:62:24:F9:71")"
# CREATE dataframe matheus - CURRENT DEVICE
dfmath = df[df["chipset"] == "AE:08:62:24:F9:71"]
dffake = df[df["chipset"] == "GREEN DASHBOARD TEST"]


# Acquisitions with date and time format different than "21/04/20" and "0:11:20" will not work

# TODO create for loop for different dataframes
df1 = dfmath.iloc[10]
df2 = dfmath.iloc[11]
# dfn = dfmath.iloc[n] 


dff1 = dffake.iloc[0]

#df3 = dffake.iloc[0:3]

# dfmath.values turns a data frame into an array for better management
#If needed, here is the documentation https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html


# Constructor method gets the array and returns a container object
# TODO create for loop to create different containers
instancy = Container(df1)

instancy2 = Container(df2)

instancy3 = Container(dff1)


# Pandas.DataFrame has a lot of useful methods, like "to_csv" and "to_excel".
# This function gets the container object and returns a DataFrame object
# TODO create for loop to create different new dataframes
new_data_frame = instancy.to_DataFrame()
new_data_frame = new_data_frame.append(instancy2.to_DataFrame())
new_data_frame = new_data_frame.append(instancy3.to_DataFrame())
print(new_data_frame)

# Exporting to a .csv file without zipping
#new_data_frame.to_csv("CSV.csv", index = False)
new_data_frame.to_excel("output.xlsx")

