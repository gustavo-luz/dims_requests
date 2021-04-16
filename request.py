import json
import requests



base = "http://uiot-dims.herokuapp.com/list/data"
chipset = "AE:08:62:24:F9:71" 
url = base + "?chipset=" + chipset 
print(url)

r = requests.get(url)
content = json.loads(r.content)
print(type(content))
#print(content)

#observations desired: change this to see more data
n = 5
# first obs: change this to change the starting point
f = 5
# individual obs (for current sending)
n = (3 * n)+f
# see content
new = []
for i in range(f,n):
    print(content[i]['value'])
    # append values to empty list
    new.append(content[i]['value'])

print(new)
#TODO join lists 3 by 3
#s = ''.join(new)



