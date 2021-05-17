import requests
import pandas as pd
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Class 'Container' holds information and handles manipulation of the data
# It's recommended to use 'array_of_containers = Container.to_container(dataFrame)' instead of using class contructor method
class Container:

    # Maximum container's height
    _MAX_DISTANCE = 160.0 

    # It receives a 'dataFrame' object and returns an array of 'Container' objects with the same size 
    def to_container(df):
        array = []
        data_size = df.value.size

        for i in range(data_size):
            array += [Container(df.iloc[i])]

        return array



    # Since we are dealing with arrays of 'Container' objects, it's useful to move everything to a 'dataFrame' format easier
    # It receives an array of 'Container' objects and return a 'dataFrame' with all of their information
    def array_to_dataFrame(array, id_dictionary):
        df  = pd.DataFrame()

        for cont in array:
            df = df.append(cont._container_to_DataFrame(id_dictionary))

        return df



    # This function receives a Container object and returns a dataFrame back
    # Must be given the sheets object managing the script
    def _container_to_DataFrame(self, sheets):

        # These indexes are chosen from the dictionary of ids in the sheets object
        _ID_INDEX = 0
        _DESCRIPTION_INDEX = 1
        _LOCATION_INDEX = 2

        try:
            row = sheets.id_dictionary[self.mac]
        except:
            print('mac ' + self.mac + ' not registered')
            return None

        d = {'ID': row[_ID_INDEX], 'Description': row[_DESCRIPTION_INDEX], 'Capacity': [self.capacity], 'Battery': [self.battery], 
        'Date (DD/MM/YY)': [self.date.strftime("%d/%m/%y")], 'Time (HH/MM/SS)': [self.time.strftime("%H:%M:%S")],
        'Location (Latitude, Longitude)' : row[_LOCATION_INDEX]}

        # This line updates the last record of a container
        if row[_ID_INDEX] not in sheets.last_call_dictionary:
            sheets.last_call_dictionary[row[_ID_INDEX]] = d

        return pd.DataFrame(data = d)



    # This is the constructor method. It must take a dataFrame object with only one row of the original dataFrame.
    def __init__(self, dataFrame):

        # Splits the string in "value" into an array os strings
        value_aux = dataFrame['value'][0].split(",")

        self.chipset = dataFrame['chipset']
        self.mac = dataFrame['mac']
        self.distance = float(dataFrame['Distance'])
        self.battery =  dataFrame['Battery']

        self.date = datetime.datetime.strptime(dataFrame['Date'], "%y/%m/%d")
        self.time = datetime.datetime.strptime(dataFrame['Time'], "%H:%M:%S")

        # Be aware of max distance. Values above '_MAX_DISTANCE' in distance will cause negative capacity.
        self.capacity = round(100 * (1 - (self.distance / self._MAX_DISTANCE)))



# This class deals with google docs update and authentication and heroku's app request
class Sheets():


    def sheets_authentication(self):

        scope = ['https://spreadsheets.google.com/feeds']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('mimetic-parity-311801-01a924f481ab.json', scope)
        gc = gspread.authorize(credentials)
        return gc.open_by_key('1XL8hE1ve3aFKS_Gu0fIwQhNN2BXPnBr0Xv7x9rkrDqY')



    # Acquisitions with date and time format different than "21/04/20" and "0:11:20" will not work  
    def heroku_to_dataframe(self, tag):
        url = "http://uiot-dims.herokuapp.com/list/data"
        r = requests.get(url)
        content = r.json()
        df = pd.DataFrame.from_dict(content)
        df = df[df['tag'] == tag]


        distance = pd.Series([])
        battery = pd.Series([])
        date = pd.Series([])
        time = pd.Series([])

        df.insert(3, 'Distance', None, allow_duplicates = True)
        df.insert(4, 'Battery', None, allow_duplicates = True)
        df.insert(5, 'Date', None, allow_duplicates = True)
        df.insert(6, 'Time', None, allow_duplicates = True)

        for i in range(len(df)):
            df['Distance'].iloc[i], df['Battery'].iloc[i], df['Date'].iloc[i], df['Time'].iloc[i] = df['value'].iloc[i][0].split(',')


        df1 = df[df['Date'] > self.last_call_date['Date']]
        df2 = df[df['Date'] == self.last_call_date['Date']]
        df2 = df2[df2['Time'] > self.last_call_date['Time']]

        return df1.append(df2)



    # This function gets information from id's page and turn into a useful dictionary to make easier manage other data manipulations
    def _get_id_dictionary(self):
        id_dictionary = self.spreadsheet.worksheet('[Template] ID').get_all_records()

        final_dictionary = {}
        for d in id_dictionary:
            final_dictionary[d['mac']] = [d['ID'], d['Description'], d['Location (Latitude, Longitude)']]

        return final_dictionary

    def _define_last_call_time(self):
        _LAST_RECORDS_PAGE_NAME = '[Template] Dados_Historicos'

        last_records_worksheet = self.spreadsheet.worksheet(_LAST_RECORDS_PAGE_NAME)

        df = pd.DataFrame(last_records_worksheet.get_all_records())

        last_date_aux = df['Date (DD/MM/YY)'][0]
        last_time = df['Time (HH/MM/SS)'][0]

        last_date = last_date_aux[6:8] + last_date_aux[2:6] + last_date_aux[0:2]

        dic = { 'Date' : last_date, 'Time' : last_time}

        return dic

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



    # The initializer method deals with authenticating google docs and inicializing necessary dictionaries
    def __init__(self):
        self.last_call_dictionary = {}

        self.spreadsheet = self.sheets_authentication()

        self.id_dictionary = self._get_id_dictionary()

        self.last_call_date = self._define_last_call_time()