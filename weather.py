#!/usr/bin/python

#Importing the neccessary additions
from sense_hat import SenseHat
import time
import sys
import MySQLdb
import subprocess
from functions import dolog,dbdroptable,dbcreatewstables,dbcreatewdtables,db_ws_insert,db_wd_insert,dbfetch

#Declaring variables for processes checking
main_proc = None
analyzer_proc = None
scheduled_proc = None

#This is a variable with option to reset everything on startup
resetall = 0

if resetall == 1:
    #Connecting to database and creating the tables needed, and dropping existing ones if there already
    dbdroptable('weather_data')
    dbdroptable('weather_settings')
    dbcreatewstables()
    dbcreatewdtables()
    db_ws_insert('0','0','0','0','0','0','0','0')

#Running the Main script which analyzes the data and sets irrigation timer accordingly
try:
    if main_proc is not None and main_proc.poll() is None:
         print('process is already running')
    else:
        main_proc = subprocess.Popen(['/home/pi/GardenBrain/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        dolog("Starting main GardenBrain script succeeded in weather.py")
        
    time.sleep(1)
    
except:
    dolog("Starting main GardenBrain script failed in weather.py")

#Startng analyzer script in the background which updates the weather_settings table with accurate irrigation times
try:
    if analyzer_proc is not None and analyzer_proc.poll() is None:
         print('process is already running')
    else:
        analyzer_proc = subprocess.Popen(['/home/pi/GardenBrain/analyzer.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        dolog("Starting analyzer script succeeded in weather.py")
    time.sleep(1)
    
except:
    dolog("Starting analyzer script failed in weather.py")

#Startng scheduled tasks script in the background which wait for database values to start irrigation or reboot the system
try:
    if scheduled_proc is not None and scheduled_proc.poll() is None:
         print('process is already running')
    else:
        scheduled_proc = subprocess.Popen(['/home/pi/GardenBrain/scheduled.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        dolog("Starting scheduled tasks script succeeded in weather.py")
    time.sleep(1)
    
except:
    dolog("Starting scheduled tasks script failed in weather.py")

#Clearing any data on the SenseHat
sense = SenseHat()
sense.clear()

try:
    
    #Running the main weather monitor loop
    while True:

	    #Printing a blank row
        print(" ")

	    #Printing date and time
        print("The date and time is: ",time.strftime("%Y-%m-%d %H:%M"))
	
	    #Getting temperature from the SenseHat and printing the value
        temp = sense.get_temperature()
        temp = round(temp, 1)
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
            dolog("Failed to get current pressure, instead using the pressure from previous entry in database")
            
        if humidity == 0:
            humidity = dbfetch("HUMIDITY","weather_date")
            dolog("Failed to get current humidity, instead using the humidity from previous entry in database")

	    #Connecting to database again and writing the data into the weather_data table
        #db_wd_insert(time.strftime("%Y-%m-%d %H:%M"),str(temp),str(humidity),str(pressure))
        db = MySQLdb.connect("localhost”,”user”,”pass”,”weather" )
        cursor = db.cursor()
        
        try:
            cursor.execute("""INSERT INTO weather_data VALUES (%s,%s,%s,%s)""",(time.strftime("%Y-%m-%d %H:%M"),str(temp),str(humidity),str(pressure)))
            db.commit()
        except:
            db.rollback()
            
        db.close()
        dolog("Written weather data to database in weather.py")

	    #Waiting for a set number of seconds before checking data and writing to database again
        time.sleep(299)

except KeyboardInterrupt:
    pass
    time.sleep(1)
    print(" ")
    print("Aborting weather script due to keyboard interrupt")
