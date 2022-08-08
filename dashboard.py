
from operator import index
import requests
import pandas as pd
import datetime
from datetime import datetime
import numpy as np

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ast

class Sheets():

    # Handles authentication from gspread library
    def sheets_authentication(self):

        scope = ['https://spreadsheets.google.com/feeds']

        authentication_document = 'mimetic-parity-311801-01a924f481ab.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(authentication_document, scope)
        gc = gspread.authorize(credentials)
        return gc.open_by_key('1XL8hE1ve3aFKS_Gu0fIwQhNN2BXPnBr0Xv7x9rkrDqY')

    def filter_df_invalid_data(self,df):

        for i in range(len(df)):
            try:

                # 'Distance' validation
                if int(float(df['Distance'].iloc[i])) > self._MAX_DISTANCE or int(float(df['Distance'].iloc[i])) <= 0:
                    print('Invalid value: Maximum "Distance" value must be ' + str(self._MAX_DISTANCE) + ' cm. Not: '+ df['Distance'].iloc[i] )
                    print('Date and Time of error: ' +  df['Date'][i] + ' ' + df['Time'][i])
                    print(f'dropping row: {i}')
                    df.loc[i] = np.nan
                    


                # 'Battery' validation
                if int(float(df['Battery'].iloc[i])) > 100 or int(float(df["Battery"].iloc[i])) < 0:
                    print('Invalid value: Maximum "Battery" value must be 100')
                    print('Date and Time of error: ' +  df['Date'][i] + ' ' + df['Time'][i])
                    df.loc[i] = np.nan

                # 'mac' validation
                if df['mac'].iloc[i] not in self.id_dictionary:
                    print('Invalid value: Mac ' + df['mac'].iloc[i] + ' not registered, please add in worksheet "[Template] ID"')
                    print('Date and Time of error: ' +  df['Date'][i] + ' ' + df['Time'][i])
                    print(f'dropping row: {i}')
                    df.loc[i] = np.nan

            except:
                print(f'error with {i}')

        #drop NaN values that were set to invalid rows: 
        df = df.dropna(axis = 0, how = 'all')
        print(df)
        return df


    # Acquisitions with respectively date and time format different than "21/04/20" and "0:11:20" will not work  
    def heroku_to_dataframe(self, tag_list):
        oldurl = "http://dims.uiot.redes.unb.br/list/data"

        url = "http://200.130.75.146/list/data"

        r = requests.get(url)
        content = r.json()
        df = pd.DataFrame.from_dict(content)

        # These two lines filter the given dataframe based on "tags" column
        mask = df['tags'].apply(pd.Series).isin(tag_list).sum(axis=1) > 0
        df_rtt = df['tags'].apply(pd.Series).isin(tag_list).sum(axis=1) > 0

        
        df = df[(mask)]
        df = df.dropna(subset=['serverTime'])
        final_df = pd.DataFrame()
        
        
        distance = pd.Series([])
        battery = pd.Series([])
        date = pd.Series([])
        time = pd.Series([])

        #Convert from list with lenght 1 to 4, reestructure string
        for i in range (len(df['value'])):
            df['value'].iloc[i] = df['value'].iloc[i][0].split(',')
            #print(df['value'].iloc[i])

        print(df)
        df.reset_index(drop=True, inplace=True)

        df_split = pd.DataFrame(df['value'].to_list(), columns = ['Distance', 'Battery', 'Latitude','Longitude'])
        print(df_split)
        df = pd.concat([df, df_split], axis=1)
        print (df)

        #It creates new columns based on column "values" for better managing data
        df['Date'] = ''
        df['Time'] = ''
        for i in range(len(df)):


            timestamp_array = df['serverTime'].iloc[i]
            timestamp_array = timestamp_array[:19]
            timestamp = datetime.strptime(timestamp_array, '%Y-%m-%dT%H:%M:%S')
            
            df['Date'].iloc[i] = timestamp_array
            df['Date'].iloc[i] = timestamp.strftime("%m/%d/%y")
            df['Time'].iloc[i] = timestamp.strftime("%H:%M:%S")
            
        df.to_csv('unfiltered_df.csv')
        df = self.filter_df_invalid_data(df)
        final_df = df
        return final_df
    
    #TODO use only heroku_to_dataframe function with one parameter of voltage
    def voltage_to_dataframe(self, tag_list):
        oldurl = "http://dims.uiot.redes.unb.br/list/data"

        url = "http://200.130.75.146/list/data"

        r = requests.get(url)
        content = r.json()
        df = pd.DataFrame.from_dict(content)

        # These two lines filter the given dataframe based on "tags" column
        mask = df['tags'].apply(pd.Series).isin(tag_list).sum(axis=1) > 0
        
        df = df[(mask)]
        df = df.dropna(subset=['serverTime'])
        final_df = pd.DataFrame()
        
        #EG: {"chipset":"Green1","mac":"9F:43:45:5F:F1:42","serverTime":"2022-07-05T03:37:18.586414","serviceNumber":0,"tags":["rtt"],"value":["298"]},

        #Convert from list with lenght 1 to 4, reestructure string
        for i in range (len(df['value'])):
            df['value'].iloc[i] = df['value'].iloc[i][0]
            #print(df['value'].iloc[i])

        print(df)
        df.reset_index(drop=True, inplace=True)
        df.to_csv('RTT_full_df.csv')

        
        #It creates new columns based on column "values" for better managing data
        df['Date'] = ''
        df['Time'] = ''
        for i in range(len(df)):


            timestamp_array = df['serverTime'].iloc[i]
            timestamp_array = timestamp_array[:19]
            timestamp = datetime.strptime(timestamp_array, '%Y-%m-%dT%H:%M:%S')
            
            df['Date'].iloc[i] = timestamp_array
            df['Date'].iloc[i] = timestamp.strftime("%m/%d/%y")
            df['Time'].iloc[i] = timestamp.strftime("%H:%M:%S")

        #ADD another function if rtt filtering is needed
        #df = self.filter_df_invalid_data(df)
        df.to_csv('RTT_full_df.csv')
        final_df = df
        return final_df


    # This dictionary will return ID, Description and location of a container based on it's mac
    def _get_mac_id_dictionary(self):
        initial_dictionary = self.spreadsheet.worksheet('[Template] ID').get_all_records()

        final_dictionary = {}
        for d in initial_dictionary:
            final_dictionary[d['mac']] = [d['ID'], d['Description'], d['Location (Latitude, Longitude)']]
        
        return final_dictionary


    # This dictionary will return last recorded time based on containers ID
    # It helps to know wich data from heroku's should be uploaded to spreadsheets
    def _get_id_recent_call_dictionary(self):
        initial_dictionary = self.spreadsheet.worksheet('[Template] Dados_Recentes').get_all_records()

        final_dictionary = {}
        for d in initial_dictionary:
            final_dictionary[d['ID']] = [d['Date (DD/MM/YY)'], d['Time (HH/MM/SS)']]
        
        return final_dictionary

    # This function uploads information to google docs pages
    def upload_to_google(self, all_records_dataFrame):
        _ALL_RECORDS_PAGE_NAME = '[Template] Dados_Historicos'
        _LAST_RECORDS_PAGE_NAME = '[Template] Dados_Recentes'

        all_records_worksheet = self.spreadsheet.worksheet(_ALL_RECORDS_PAGE_NAME)
        last_records_worksheet = self.spreadsheet.worksheet(_LAST_RECORDS_PAGE_NAME)

        # This for statement deals with finding wich row to update in most recent record's page
        for instance in self.last_call_dictionary:
            cell = last_records_worksheet.find(instance)
            df = pd.DataFrame(self.last_call_dictionary[instance])

            last_records_worksheet.update(cell.address, df.values.tolist())

        all_records_worksheet.insert_rows(all_records_dataFrame.values.tolist(), 2)

#TODO use only format_data_frame function with one parameter of voltage, debug to create past_data_sheet TRue mode or simmilar work
    # This function uploads information to google docs pages
    def upload_to_google_rtt(self, all_records_dataFrame,recent_table_sheet,past_data_sheet=False):
        _ALL_RECORDS_PAGE_NAME = recent_table_sheet
        

        all_records_worksheet = self.spreadsheet.worksheet(_ALL_RECORDS_PAGE_NAME)
        
        if past_data_sheet == True:
        # This for statement deals with finding wich row to update in most recent record's page
            _LAST_RECORDS_PAGE_NAME = past_data_sheet
            last_records_worksheet = self.spreadsheet.worksheet(_LAST_RECORDS_PAGE_NAME)

            for instance in self.last_call_dictionary:
                cell = last_records_worksheet.find(instance)
                df = pd.DataFrame(self.last_call_dictionary[instance])

                last_records_worksheet.update(cell.address, df.values.tolist())

        # upload to sheets last records
        all_records_worksheet.insert_rows(all_records_dataFrame.values.tolist(), 2)



    # Returns a new dataFrame with data format used in spreadsheets
    def format_data_frame(self, df): 

        # An empty dataFrame
        final_dataframe = pd.DataFrame()

        for i in range(len(df)):

            # These variables manage information that will be used in the final dataframe
            ID, description, location = self.id_dictionary[df['mac'].iloc[i]]
            capacity = 1 - (float(df['Distance'].iloc[i]) / self._MAX_DISTANCE)
            battery = float(df['Battery'].iloc[i])/100
            date = df['Date'].iloc[i]
            time = df['Time'].iloc[i]

            # d is a dictionary where strings are indexe's and it's respective values
            d = {'ID' : ID, 'Description': description, 'Capacity': capacity, 'Battery' : battery, 'Date (DD/MM/YY)': date,
            'Time (HH/MM/SS)' : time, 'Location (Latitude, Longitude)' : location}

            # df_aux is a dataFrame based on dictionary 'd'
            df_aux = pd.DataFrame(data = d, index = [0])

            final_dataframe = final_dataframe.append(df_aux)

            if ID not in self.last_call_dictionary:
                self.last_call_dictionary[ID] = df_aux

        return final_dataframe

 #TODO use only format_data_frame function with one parameter of voltage
   
    def format_data_frame_rtt(self, df): 

        # An empty dataFrame
        final_dataframe = pd.DataFrame()

        for i in range(len(df)):

            # These variables manage information that will be used in the final dataframe
            ID, description, location = self.id_dictionary[df['mac'].iloc[i]]
            voltage = float(df['value'].iloc[i])
            date = df['Date'].iloc[i]
            time = df['Time'].iloc[i]

            # d is a dictionary where strings are indexe's and it's respective values
            d = {'ID' : ID, 'Description': description, 'Voltage' : voltage, 'Date (DD/MM/YY)': date,
            'Time (HH/MM/SS)' : time, 'Location (Latitude, Longitude)' : location}

            # df_aux is a dataFrame based on dictionary 'd'
            df_aux = pd.DataFrame(data = d, index = [0])

            final_dataframe = final_dataframe.append(df_aux)

            if ID not in self.last_call_dictionary:
                self.last_call_dictionary[ID] = df_aux

        return final_dataframe


    # The initializer method deals with authenticating google docs and inicializing necessary dictionaries
    def __init__(self):
        self._MAX_DISTANCE = 160.0
        #self.data_validation()
        # This dictionary handles last recorded data from the containers, that will be uploaded to worksheet '[Template] Dados_Recentes'
        self.last_call_dictionary = {}               

        try:
            self.spreadsheet = self.sheets_authentication()

            self.id_dictionary = self._get_mac_id_dictionary()

            self.id_recent_call_dictionary = self._get_id_recent_call_dictionary()
        except:
            print("Error authenticating, please include credential files")