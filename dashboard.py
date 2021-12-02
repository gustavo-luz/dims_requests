
import requests
import pandas as pd
import datetime
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheets():

    # Handles authentication from gspread library
    def sheets_authentication(self):

        scope = ['https://spreadsheets.google.com/feeds']

        authentication_document = 'mimetic-parity-311801-01a924f481ab.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(authentication_document, scope)
        gc = gspread.authorize(credentials)
        return gc.open_by_key('1XL8hE1ve3aFKS_Gu0fIwQhNN2BXPnBr0Xv7x9rkrDqY')


    def data_validation(self, df):

        # Instance_mac will hold the mac number of currently instancy of the dataFrame. 
        instance_mac = df['mac']

        # Only registered container's information must be uploaded.
        if instance_mac not in self.id_dictionary:
            print('Invalid value: Mac ' + instance_mac + ' not registered, please add in worksheet "[Template] ID"')
            print('Date and Time of error: ' +  df['Date'] + ' ' + df['Time'])


            # VER DPS


            return False

        value_array = df['value'][0].split(',')

        # 'value' column has to follow the format: "Distance,Battery"
        if  len(value_array)  != 2:
            print(value_array)
            print('Invalid sintaxe: "Value" format must be "Distance,Battery"')
            return False


        if len(df['time'])  == 26:

            timestamp_array = df['time']
            timestamp_array = timestamp_array[:-7]

            timestamp = datetime.strptime(timestamp_array, '%Y-%m-%dT%H:%M:%S')

            date_array = timestamp.strftime("%m/%d/%y")
            time_array = timestamp.strftime("%H:%M:%S")

            print(timestamp_array,date_array,time_array)    

            df['Distance'], df['Battery'] = value_array
            df['Date'] = date_array
            df['Time'] = time_array


            # 'Distance' validation
            if int(df['Distance']) > self._MAX_DISTANCE or int(df['Distance']) <= 0:
                print('Invalid value: Maximum "Distance" value must be ' + str(self._MAX_DISTANCE) + ' cm.')
                print('Date and Time of error: ' +  df['Date'] + ' ' + df['Time'])
                return False


            # 'Battery' validation
            if int(df['Battery']) > 100 or int(df["Battery"]) < 0:
                print('Invalid value: Maximum "Battery" value must be 100')
                print('Date and Time of error: ' +  df['Date'] + ' ' + df['Time'])
                return False
            
            return True
        else:
            print("Invalid timestamp")




    # Acquisitions with respectively date and time format different than "21/04/20" and "0:11:20" will not work  
    def heroku_to_dataframe(self, tag_list):
        url = "http://dims.uiot.redes.unb.br/list/data"
        r = requests.get(url)
        content = r.json()
        df = pd.DataFrame.from_dict(content)

        # These two lines filter the given dataframe based on "tags" column
        mask = df['tags'].apply(pd.Series).isin(tag_list).sum(axis=1) > 0
        df = df[(mask)]

        final_df = pd.DataFrame()
        

        distance = pd.Series([])
        battery = pd.Series([])
        date = pd.Series([])
        time = pd.Series([])

        df.insert(3, 'Distance', None, allow_duplicates = True)
        df.insert(4, 'Battery', None, allow_duplicates = True)
        df.insert(5, 'Date', None, allow_duplicates = True)
        df.insert(6, 'Time', None, allow_duplicates = True)


        print (df)
        #It creates new columns based on column "values" for better menaging data
        for i in range(len(df)):

            if not self.data_validation(df.iloc[i]):
                continue

            timestamp_array = df['time'].iloc[i]
            timestamp_array = timestamp_array[:18]

            timestamp = datetime.strptime(timestamp_array, '%Y-%m-%dT%H:%M:%S')

            df['Distance'].iloc[i], df['Battery'].iloc[i] = df['value'].iloc[i][0].split(',')
            df['Date'].iloc[i] = timestamp.strftime("%m/%d/%y")
            df['Time'].iloc[i] = timestamp.strftime("%H:%M:%S")

            df['Distance'].iloc[i], df['Battery'].iloc[i] = df['value'].iloc[i][0].split(',')

            id = self.id_dictionary[df['mac'].iloc[i]][0]
            recent_call = self.id_recent_call_dictionary[id]

            if(df['Date'].iloc[i] == recent_call[0] and df['Time'].iloc[i] == recent_call[1]):
                df = df.iloc[:i]
                break
            
            d = {'chipset' : df['chipset'].iloc[i], 'Mac' : df['mac'].iloc[i], 'Distance' : df['Distance'].iloc[i], 'Battery' : df['Battery'].iloc[i], 'Date' : df['Date'].iloc[i], 'Time' : df['Time'].iloc[i]}
            final_df = final_df.append(pd.DataFrame(data = d, index = [0]))
        
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



    # Returns a new dataFrame with data format used in spreadsheets
    def format_data_frame(self, df): 

        # An empty dataFrame
        final_dataframe = pd.DataFrame()

        for i in range(len(df)):

            # These variables manage information that will be used in the final dataframe
            ID, description, location = self.id_dictionary[df['Mac'].iloc[i]]
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




    # The initializer method deals with authenticating google docs and inicializing necessary dictionaries
    def __init__(self):
        self._MAX_DISTANCE = 160.0
        #self.data_validation()
        # This dictionary handles last recorded data from the containers, that will be uploaded to worksheet '[Template] Dados_Recentes'
        self.last_call_dictionary = {}               

        self.spreadsheet = self.sheets_authentication()

        self.id_dictionary = self._get_mac_id_dictionary()

        self.id_recent_call_dictionary = self._get_id_recent_call_dictionary()
