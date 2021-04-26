import requests
import pandas as pd
import datetime

# Class 'Container' holds information and handles manipulation of the data
# A 'container' object must not be created using through it's contructor method, but by using 'Container.to_container(dataFrame)'
# The advantage of doing so is that 'to_container' can return an array of containers when given a bigger 'dataFrame' object instead of only working with a single row 'dataFrame'
# Constructor method can still be used, since python can't make private methods. If needed, another argument must be given: 
# 'new_container = Container(dataFrame, permission = True)' But be aware, it only receives a single row 'dataFrame' object.
# The creation of an object makes easier to give maintenance to the code if another kind of manipulation of the data is needed and still use features from useful classes like datetime

class Container:
    _MAX_DISTANCE = 160.0
    _DISTANCE_INDEX = 0
    _BATTERY_INDEX = 1
    _DATE_INDEX = 2
    _TIME_INDEX = 3

    # This is the function whe're going to use. It receives a 'dataFrame' object and returns an array of 'Container' objects with the same size 
    def to_container(df):
        array = []
        data_size = df.value.size

        for i in range(data_size):
            array += [Container(df.iloc[i], permission = True)]

        return array


    # Since we are dealing with arrays of 'Container' objects, it's useful to move everything to a 'dataFrame' format easier
    # It receives an array of 'Container' objects and return a 'dataFrame' with all of their information
    def array_to_dataFrame(array):
        df  = pd.DataFrame()

        for cont in array:
            df = df.append(cont._container_to_DataFrame())
            
        return df


    # The class dataFrame bring some interesting features. 
    # This function receives a Container object and returns a dataFrame back
    #TODO CONVERTER YY/MM/DD 
    def _container_to_DataFrame(self):
        d = {'chipset': [self.chipset], 'mac': [self.mac], 'serviceNumber': [self.service],
        'capacity': [self.capacity], 'battery': [self.battery], 
        'date': [self.date.strftime("%d/%m/%y")], 'time': [self.time.strftime("%H:%M:%S")]}
        return pd.DataFrame(data = d)

    # This is the constructor method. It must take a dataFrame object with only one row of the original dataFrame.
    # 'info' is a dataFrame, that's why is possible to find values through it's keys
    # Since Python can't define private functions, the variable 'permission' makes harder creating a 'container' object using the constructor method

    def __init__(self, info, permission = False):

        if permission == False:
            print("\n\nPlease, use function 'Container.to_container(dataFrame)' to create a Container object.\n\n")
            return None

        # Splits the string in "value" into an array os strings
        value_aux = info['value'][0].split(",")
        
        self.chipset = info['chipset']
        self.mac = info['mac']
        self.service = info['serviceNumber']

        self.distance = float(value_aux[self._DISTANCE_INDEX])
        self.battery =  value_aux[self._BATTERY_INDEX]
        self.date = datetime.datetime.strptime(value_aux[self._DATE_INDEX], "%d/%m/%y")
        self.time = datetime.datetime.strptime(value_aux[self._TIME_INDEX], "%H:%M:%S")

        # Be aware of max distance. Values above '_MAX_DISTANCE' in distance will cause negative capacity.
        self.capacity = 1 - (self.distance / self._MAX_DISTANCE)
        