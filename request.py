import json
import requests
import pandas as pd

from dashboard import Container
from dashboard import Sheets

# TODO add more devices according to chipset

sheets = Sheets()

# CREATE dataframe using device's chipset
df = sheets.heroku_to_dataframe(chipset = "GREEN DASHBOARD TEST 2")
df2 = sheets.heroku_to_dataframe(chipset = "GREEN DASHBOARD TEST 3")
df = df.append(df2)

# 'Container.to_container(df)' method gets the array and returns a container object
instancy_fake = Container.to_container(df)

# A Sheets object must be given
# This function gets the 'container' array and returns a DataFrame object
full_dataFrame = Container.array_to_dataFrame(instancy_fake, sheets)
print(full_dataFrame)

sheets.upload_to_google(full_dataFrame)