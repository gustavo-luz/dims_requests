
import requests
import pandas as pd
import datetime

url = "http://uiot-dims.herokuapp.com/list/data"
r = requests.get(url)
content = r.json()
df = pd.DataFrame.from_dict(content)

tag_list=['example-tag','iisc']

mask = df['tags'].apply(pd.Series).isin(tag_list).sum(axis=1) > 0
print(df[(mask)])




