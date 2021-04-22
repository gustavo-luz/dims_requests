
# CLIENT
name: esp test
chipset: GREEN DASHBOARD TEST
mac: 81:9F:CE:53:4C:9D


curl -X POST "http://uiot-dims.herokuapp.com/client" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"name\": \"esp test\",  \"chipset\": \"GREEN DASHBOARD TEST\",  \"mac\": \"81:9F:CE:53:4C:9D\"}"

# SERVICE
number: 0
chipset: GREEN DASHBOARD TEST
mac: 81:9F:CE:53:4C:9D
name: dashboard trash1
parameter: id,data,hour,battery,capacity


curl -X POST "http://uiot-dims.herokuapp.com/service" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"number\": \"0\", \"chipset\": \"GREEN DASHBOARD TEST\", \"mac\": \"81:9F:CE:53:4C:9D\", \"name\": \"dashboard trash1\", \"parameter\": \"id,data,hour,battery,capacity\"}"

# DATA
chipset: GREEN DASHBOARD TEST
mac: 81:9F:CE:53:4C:9D
service number: 0
value: [10,60,21/04/21,13:04:05]

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST\", \"mac\": \"81:9F:CE:53:4C:9D\", \"serviceNumber\": \"0\", \"value\": [ \"10,60,22/04/21,13:40:05\"]}"


curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST\", \"mac\": \"81:9F:CE:53:4C:9D\", \"serviceNumber\": \"0\", \"value\": [ \"10,60,22/04/21,13:41:15\"]}"

curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"chipset\": \"GREEN DASHBOARD TEST\", \"mac\": \"81:9F:CE:53:4C:9D\", \"serviceNumber\": \"0\", \"value\": [ \"10,60,22/04/21,13:42:13\"]}"

IF YOU WANT TO DO MORE POSTS, JUST FOLLOW THE CURL AND CHANGE THE VALUE