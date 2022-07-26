import requests
import pandas as pd

from dashboard import Sheets

# This line surpresses a warning
pd.set_option('mode.chained_assignment', None)

sheets = Sheets()

# It dataframe using heroku's information
df = sheets.heroku_to_dataframe(tag_list = ['iisc'])

rtt_df = sheets.voltage_to_dataframe(tag_list = ['rtt'])

print(df)
# Returns a new dataFrame with data format used in spreadsheets
final_df = sheets.format_data_frame(df)
print(final_df)

final_df.to_csv('full_df.csv')

final_rtt_df = sheets.format_data_frame_rtt(rtt_df)
final_rtt_df.to_csv('full_rtt_df.csv')
# Takes the formated dataframe and posts on google spreadsheets
sheets.upload_to_google(final_df)
sheets.upload_to_google_rtt(final_rtt_df,'[VOLTAGE] Historical_Data',past_data_sheet=False)