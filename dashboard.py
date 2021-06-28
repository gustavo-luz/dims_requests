
import requests
import pandas as pd
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheets():

    # Handles authentication from gspread library
    def sheets_authentication(self):

        scope = ['https://spreadsheets.google.com/feeds']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('mimetic-parity-311801-01a924f481ab.json', scope)
        gc = gspread.authorize(credentials)
        return gc.open_by_key('1XL8hE1ve3aFKS_Gu0fIwQhNN2BXPnBr0Xv7x9rkrDqY')


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


        #It creates new columns based on column "values" for better menaging data
        for i in range(len(df)):

            # Instance_mac will hold the mac number of currently instancy of the dataFrame. 
            instance_mac = df['mac'].iloc[i]

            # This condition makes shure that only registered container's information will be uploaded.
            if instance_mac not in self.id_dictionary:
                print('Mac ' + instance_mac + ' not registered, please add in worksheet "[Template] ID"')
                continue
            
            value_array = df['value'].iloc[i][0].split(',')

            # 'value' column has to follow the format: "Distance,Battery,MM/DD/YY,HH:MM:SS"
            if  len(value_array)  != 4:
                print('"Value" component error in ' + i + 'position' + '. Wrong sitaxe')
                continue


            df['Distance'].iloc[i], df['Battery'].iloc[i], df['Date'].iloc[i], df['Time'].iloc[i] = value_array

            id = self.id_dictionary[df['mac'].iloc[i]][0]
            recent_call = self.id_recent_call_dictionary[id]


            if(df['Date'].iloc[i] == recent_call[0] and df['Time'].iloc[i] == recent_call[1]):
                df = df.iloc[:i]
                break
            
            d = {'chipset' : df['chipset'].iloc[i], 'Mac' : df['mac'].iloc[i], 'Distance' : df['Distance'].iloc[i], 'Battery' : df['Distance'].iloc[i], 'Date' : df['Date'].iloc[i], 'Time' : df['Time'].iloc[i]}
            final_df = final_df.append(pd.DataFrame(data = d, index = [0]))
        
        #print(final_df)

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
            date = d['Date (DD/MM/YY)'][6:8] + d['Date (DD/MM/YY)'][2:6] + d['Date (DD/MM/YY)'][0:2]
            final_dictionary[d['ID']] = [date, d['Time (HH/MM/SS)']]
        
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
        _MAX_DISTANCE = 160.0 

        # An empty dataFrame
        final_dataframe = pd.DataFrame()

        for i in range(len(df)):
            
            # These variables manage information that will be used in the final dataframe
            ID, description, location = self.id_dictionary[df['mac'].iloc[i]]
            capacity = 1 - (float(df['Distance'].iloc[i]) / _MAX_DISTANCE)
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
        # This dictionary handles last recorded data from the containers, that will be uploaded to worksheet '[Template] Dados_Recentes'
        self.last_call_dictionary = {}               

        self.spreadsheet = self.sheets_authentication()

        self.id_dictionary = self._get_mac_id_dictionary()

        self.id_recent_call_dictionary = self._get_id_recent_call_dictionary()
