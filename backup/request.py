import requests
import pandas as pd

from dashboard import Sheets

# This line surpresses a warning
pd.set_option('mode.chained_assignment', None)

sheets = Sheets()

# It dataframe using heroku's information
df = sheets.heroku_to_dataframe(tag_list = ['iisc'])

# Returns a new dataFrame with data format used in spreadsheets
final_df = sheets.format_data_frame(df)
print(final_df)

# Takes the formated dataframe and posts on google spreadsheets
sheets.upload_to_google(final_df)