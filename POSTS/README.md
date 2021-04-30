

## teste de crash : sem tempo
curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST\", \"mac\": \"81:9F:CE:53:4C:9D\", \"serviceNumber\": \"0\", \"value\": [ \"10,60,21/04/30\"]}"

## teste de tags
curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"tags\": [ \"teste de tag\"],\"randomparam\": \"bla\",\"chipset\": \"GREEN DASHBOARD TEST\", \"mac\": \"81:9F:CE:53:4C:9D\", \"serviceNumber\": \"0\", \"value\": [ \"10,60,21/04/30\"],\"randomparam2\": \"blabla\"}"

IF YOU WANT TO DO MORE POSTS, JUST FOLLOW THE CURL AND CHANGE THE VALUE


# CLIENT
name: esp test
chipset: GREEN DASHBOARD TEST 2
mac: 9C:E5:69:89:DC:2B


curl -X POST "http://uiot-dims.herokuapp.com/client" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"name\": \"esp test\",  \"chipset\": \"GREEN DASHBOARD TEST 2\",  \"mac\": \"9C:E5:69:89:DC:2B\"}"

# SERVICE
number: 0
chipset: GREEN DASHBOARD TEST 2
mac: 9C:E5:69:89:DC:2B
name: dashboard trash2
parameter: id,data,hour,battery,capacity


curl -X POST "http://uiot-dims.herokuapp.com/service" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"number\": \"0\", \"chipset\": \"GREEN DASHBOARD TEST 2\", \"mac\": \"9C:E5:69:89:DC:2B\", \"name\": \"dashboard trash2\", \"parameter\": \"id,data,hour,battery,capacity\"}"


# DATA
chipset: GREEN DASHBOARD TEST 2
mac: 9C:E5:69:89:DC:2B
service number: 0
value: [10,60,21/04/21,13:04:05]

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 2\", \"mac\": \"9C:E5:69:89:DC:2B\", \"serviceNumber\": \"0\", \"value\": [ \"40,90,21/04/30,16:47:05\"]}"


curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 2\", \"mac\": \"9C:E5:69:89:DC:2B\", \"serviceNumber\": \"0\", \"value\": [ \"35,86,21/04/30,16:48:05\"]}"

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 2\", \"mac\": \"9C:E5:69:89:DC:2B\", \"serviceNumber\": \"0\", \"value\": [ \"35,84,21/04/30,16:49:25\"]}"

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 2\", \"mac\": \"9C:E5:69:89:DC:2B\", \"serviceNumber\": \"0\", \"value\": [ \"30,80,21/04/30,17:10:25\"]}"

# GREEN DASHBOARD TEST 3

# CLIENT
name: esp test
chipset: GREEN DASHBOARD TEST 3
mac: 67:98:1D:FD:FE:39


curl -X POST "http://uiot-dims.herokuapp.com/client" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"name\": \"esp test\",  \"chipset\": \"GREEN DASHBOARD TEST 3\",  \"mac\": \"67:98:1D:FD:FE:39\"}"

# SERVICE
number: 0
chipset: GREEN DASHBOARD TEST 3
mac: 67:98:1D:FD:FE:39
name: dashboard trash3
parameter: id,data,hour,battery,capacity


curl -X POST "http://uiot-dims.herokuapp.com/service" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"number\": \"0\", \"chipset\": \"GREEN DASHBOARD TEST 3\", \"mac\": \"67:98:1D:FD:FE:39\", \"name\": \"dashboard trash3\", \"parameter\": \"id,data,hour,battery,capacity\"}"


# DATA
chipset: GREEN DASHBOARD TEST 3
mac: 67:98:1D:FD:FE:39
service number: 0
value: [10,60,21/04/21,13:04:05]

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 3\", \"mac\": \"67:98:1D:FD:FE:39\", \"serviceNumber\": \"0\", \"value\": [ \"50,95,21/04/30,17:30:25\"]}"

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 3\", \"mac\": \"67:98:1D:FD:FE:39\", \"serviceNumber\": \"0\", \"value\": [ \"45,90,21/04/30,17:32:35\"]}"

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 3\", \"mac\": \"67:98:1D:FD:FE:39\", \"serviceNumber\": \"0\", \"value\": [ \"40,85,21/04/30,17:33:40\"]}"

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST 3\", \"mac\": \"67:98:1D:FD:FE:39\", \"serviceNumber\": \"0\", \"value\": [ \"40,85,21/04/30,17:35:40\"]}"



