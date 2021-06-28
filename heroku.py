import os
import pandas as pd
import runpy

import datetime
import requests


class Heroku:

    def _define_cmd(self, last_value, chipset, mac):
        last_date = last_value[2]
        last_time = last_value[3]
        last_distance = int(last_value[0])
        last_battery = int(last_value[1])

        if(last_distance < 10):
            later_distance = '160'
        else:
            later_distance = str(last_distance - 5)
        
        if(last_battery < 10):
            later_battery = '100'
        else:
            later_battery = str(last_battery - 1)

        date = datetime.datetime.strptime(last_date, "%m/%d/%y")
        time = datetime.datetime.strptime(last_time, "%H:%M:%S")

        if(last_time > '23:29:59'):
            later_date = date + datetime.timedelta(days = 1)
        else:
            later_date = date

        later_time = time + datetime.timedelta(minutes = 30)

        date_str = later_date.strftime("%m/%d/%y")
        time_str = later_time.strftime("%H:%M:%S")

        later_value = '[    \\"' + later_distance + ','+ later_battery + ',' + date_str + ',' + time_str + '\\"  ]}"'

        return 'curl -X POST "http://dims.uiot.redes.unb.br/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \\"tags\\": [      \\"iisc\\"    ],  \\"chipset\\": \\"' + chipset + '\\",  \\"mac\\": \\"' + mac + '\\",  \\"serviceNumber\\": 1,  \\"value\\": ' + later_value


    def _update_heroku(self, chipset):

        url = "http://dims.uiot.redes.unb.br//list/data"
        r = requests.get(url)
        content = r.json()
        df = pd.DataFrame.from_dict(content)

        df = df[df['chipset'] == chipset]
        last_value = df['value'].iloc[0][0].split(',')
        mac = df['mac'].iloc[0]

        cmd_str = self._define_cmd(last_value, chipset, mac)

        print(cmd_str)
        #os.system(cmd_str)

    def update_heroku(self, chipsets, n = 1):
        for i in range(n):
            for chipset in chipsets:
                self._update_heroku(chipset = chipset)

    def run_main():
        runpy.run_path('request.py')
