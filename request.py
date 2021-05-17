import json
import requests
import pandas as pd

from dashboard import Container
from dashboard import Sheets

pd.set_option('mode.chained_assignment', None)

# TODO add more devices according to chipset
sheets = Sheets()

# CREATE dataframe using device's chipset
df = sheets.heroku_to_dataframe(tag = 'iisc')

# 'Container.to_container(df)' method gets the array and returns a container object
instancy_fake = Container.to_container(df)

# A Sheets object must be given
# This function gets the 'container' array and returns a DataFrame object
full_dataFrame = Container.array_to_dataFrame(instancy_fake, sheets)


sheets.upload_to_google(full_dataFrame)

#Fazer a apresentação
# Lembrar de avisar para não colocar a apresentação em um looping para não extrapolar o ano de 2099. O formato só cobre duas casas decimais.

# TO-DO:
# Subscripe new containers when given new macs
# Also update battery and capacity
# Make heroku.py update every container using recent call data page to know wich macs to get
# Make heroku.py use last calls from heroku instead of spreadsheets