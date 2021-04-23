import requests
import pandas as pd
import datetime

# Class Conteiner holds information of the and handles manipulation of the data

class Container:
    #TODO define final max distance
    _MAX_DISTANCE = 160.0
    _DISTANCE_INDEX = 0
    _BATTERY_INDEX = 1
    _DATE_INDEX = 2
    _TIME_INDEX = 3

    # The class dataFrame bring some interesting features. 
    # This function receives a Container object and returns a dataFrame back
    def to_DataFrame(self):
        #TODO remove servicenumber? define final collumns
        d = {'chipset': [self.chipset], 'mac': [self.mac], 'serviceNumber': [self.service],
        'capacity': [self.capacity], 'battery': [self.battery], 
        'date': [self.date.strftime("%d/%m/%y")], 'time': [self.time.strftime("%H:%M:%S")]}
        return pd.DataFrame(data = d)

    # This is the constructor method. It must take a dataFrame object with only one row of the original dataFrame.
    # 'info' is a dataFrame, that's why is possible to find values through it's keys

    def __init__(self, info):
        # Splits the string in "value" into an array of strings
        value_aux = info['value'][0].split(",")
        
        self.chipset = info['chipset']
        self.mac = info['mac']
        self.service = info['serviceNumber']

        self.distance = float(value_aux[self._DISTANCE_INDEX])
        self.battery =  value_aux[self._BATTERY_INDEX]
        self.date = datetime.datetime.strptime(value_aux[self._DATE_INDEX], "%d/%m/%y")
        self.time = datetime.datetime.strptime(value_aux[self._TIME_INDEX], "%H:%M:%S")

        # Be aware of max distance. Values above 100 in distance will cause negative capacity.
        # This problem will be fixed when real max distance is defined and real values are given.
        self.capacity = 1 - (self.distance / self._MAX_DISTANCE)