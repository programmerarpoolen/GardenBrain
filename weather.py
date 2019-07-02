#!/usr/bin/python

#Importing the neccessary additions
from sense_hat import SenseHat
import time
import sys
import MySQLdb
import subprocess
from functions import dolog,dbdroptable,dbcreatewstables,dbcreatewdtables,db_ws_insert,db_wd_insert,dbfetch,keepopen,tempcorrection
import json

#Loading the JSON config file
config = json.loads(open('/var/www/html/config.json').read())

#This is a variable with option to reset everything on startup
resetall = 0

if resetall == 1:
    #Connecting to database and creating the tables needed, and dropping existing ones if there already
    dbdroptable('weather_data')
    dbdroptable('weather_settings')
    dbcreatewstables()
    dbcreatewdtables()
    db_ws_insert('0','0','0','0','0','0','0','0','0')

#Running the Main script which analyzes the data and sets irrigation timer accordingly
try:
    subprocess.Popen(['/home/pi/GardenBrain/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    dolog("Weather.py - Starting main GardenBrain script succeeded")
    time.sleep(1)
    
except:
    dolog("Weather.py - Starting main GardenBrain script failed")

#Starting analyzer script in the background which updates the weather_settings table with accurate irrigation times
try:
    subprocess.Popen(['/home/pi/GardenBrain/analyzer.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    dolog("Weather.py - Starting analyzer script succeeded")
    time.sleep(1)
    
except:
    dolog("Weather.py - Starting analyzer script failed")

#Starting scheduled tasks script in the background which wait for database values to start irrigation or reboot the system
try:
    subprocess.Popen(['/home/pi/GardenBrain/scheduled.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    dolog("Weather.py - Starting scheduled tasks script succeeded")
    time.sleep(1)
    
except:
    dolog("Weather.py - Starting scheduled tasks script failed")

#Starting hardware button script in the background which wait for hardware button push to start or stop irrigation
try:
    subprocess.Popen(['/home/pi/GardenBrain/hw_button.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    dolog("Weather.py - Starting scheduled tasks script succeeded")
    time.sleep(1)
    
except:
    dolog("Weather.py - Starting hardware button script failed")

#Clearing any data on the SenseHat
sense = SenseHat()
sense.clear()

time.sleep(5)

try:
    
    #Running the main weather monitor loop
    while True:

	    #Printing a blank row
        print(" ")

	    #Printing date and time
        print("The date and time is: ",time.strftime("%Y-%m-%d %H:%M"))
	
	    #Getting temperature from the SenseHat
        #temp = tempcorrection(sense.get_temperature())
        
        #Testing getting temperature from pressure to see if it's more accurate
        temp = tempcorrection(sense.get_temperature_from_pressure())
        print("Temperature C",temp)
        time.sleep(1)
	
	    #Getting humidity from the SenseHat and printing the value
        humidity = sense.get_humidity()
        humidity = round(humidity, 1)
        print("Humidity :",humidity)
        time.sleep(1)
	
	    #Getting pressure from the SenseHat and printing the value
        pressure = sense.get_pressure()
        pressure = round(pressure, 1)
        print("Pressure:",pressure)
        time.sleep(1)
		
	    #Showing weather data on the LED matrix (optional)
	    #sense.show_message("  Temperature " + str(temp) + "C" + "  Humidity: " + str(humidity) + "%" + "  Pressure: " + str(pressure) + "hPA", scroll_speed=(0.08), text_colour=[102,0,204])

	    #Clearing any data from the SenseHat
        sense.clear()
        
        #If fetching current pressure and humidity fails, then use previous entry in database (to remove incorrect zeros in the data)
        if pressure == 0:
            pressure = dbfetch("PRESSURE","weather_date")
            dolog("Weather.py - Failed to get current pressure, instead using the pressure from previous entry in database")
            
        if humidity == 0:
            humidity = dbfetch("HUMIDITY","weather_date")
            dolog("Weather.py - Failed to get current humidity, instead using the humidity from previous entry in database")

	    #Connecting to database again and writing the data into the weather_data table
        #db_wd_insert(time.strftime("%Y-%m-%d %H:%M"),str(temp),str(humidity),str(pressure))
        db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
        cursor = db.cursor()
        
        try:
            cursor.execute("""INSERT INTO weather_data VALUES (%s,%s,%s,%s)""",(time.strftime("%Y-%m-%d %H:%M"),str(temp),str(humidity),str(pressure)))
            db.commit()
        except:
            db.rollback()
            
        db.close()
        dolog("Weather.py - Written weather data to database")

	    #Waiting for a set number of seconds before checking data and writing to database again
        time.sleep(299)
        
        #making sure the scripts we started in the beginning of this script are still running, and restarting them if needed
        keepopen('main.py')
        keepopen('analyzer.py')
        keepopen('scheduled.py')
        keepopen('hw_button.py')

except KeyboardInterrupt:
    pass
    time.sleep(1)
    print(" ")
    print("Aborting weather script due to keyboard interrupt")
