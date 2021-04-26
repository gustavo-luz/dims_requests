import json
import requests
import pandas as pd
import gspread

from container import Container
from oauth2client.service_account import ServiceAccountCredentials

#Auth Google Sheets       
scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('mimetic-parity-311801-01a924f481ab.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open_by_key('1XL8hE1ve3aFKS_Gu0fIwQhNN2BXPnBr0Xv7x9rkrDqY')

worksheet = wks.get_worksheet(0)


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
dfmath = dfmath.iloc[10:13]



# 'Container.to_container(df)' method gets the array and returns a container object
instancy_math = Container.to_container(dfmath)
instancy_fake = Container.to_container(dffake)

# Since both instancies are arrays, you can either give them separated or concatenated
# Pandas.DataFrame has a lot of useful methods, like "to_csv" and "to_excel".
# This function gets the 'container' array and returns a DataFrame object
full_dataFrame = Container.array_to_dataFrame(instancy_math + instancy_fake)
print(full_dataFrame)

worksheet.update([full_dataFrame.columns.values.tolist()] + full_dataFrame.values.tolist())

# Exporting to .csv and .xlsx files without zipping
full_dataFrame.to_csv("output.csv", index = False)
full_dataFrame.to_excel("output.xlsx")


