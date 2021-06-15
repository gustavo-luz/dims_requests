from heroku import Heroku

# To simulate new containers, register them first at google spreadsheet's woorksheet and then add it's chipset to chipsets array
chipsets = ['GREEN DASHBOARD TEST 2', 'GREEN DASHBOARD TEST 3', 'GDT1']

heroku = Heroku()

# n is the number of new intances that will be uploaded of each simulated container
heroku.update_heroku(chipsets, n = 1)
Heroku.run_main()

# Example of a post request to heroku's app
# curl -X POST "http://uiot-dims.herokuapp.com/data" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"tags\": [      \"iisc\"    ],  \"chipset\": \"GDT1\", \"mac\": \"00:E0:4C:21:FE:31\",  \"serviceNumber\": 1,  \"value\": [    \"15,77,21/05/31,18:40:25\"  ]}"
