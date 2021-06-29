
from heroku import Heroku

# To simulate new containers, register them first at google spreadsheet's woorksheet and then add it's chipset to chipsets array
chipsets = ['GREEN DASHBOARD TEST 2', 'GREEN DASHBOARD TEST 3', 'GDT1']

heroku = Heroku()

# n is the number of new intances that will be uploaded of each simulated container
heroku.update_heroku(chipsets, n = 1)
#Heroku.run_main()