#!/usr/bin/python

# Import required Python libraries
from datetime import datetime, time
import time as t
import MySQLdb
from functions import dbfetch,dbupdate,minutedata,averager,getseconds,dolog,pressurecompare,write_weather
        
#Sleeping for 2 seconds
t.sleep(2)

try:

    #This script should be on a loop running once every 15 minutes or so
    while True:

        #Start with collecting the data for the last 15 minutes
        temperature = minutedata('TEMPERATURE')
        humidity = minutedata('HUMIDITY')
        pressure = minutedata('PRESSURE')
        dolog("Weather data received from database in analyzer.py")
        
        #Sleeping for a second
        t.sleep(1)

        #Get the average temperature, humidity and pressure for those 15 minutes
        temp_average = averager(temperature)
        humid_average = averager(humidity)
        press_average = averager(pressure)
        dolog("Weather data averaged in analyzer.py")
        
        #Sleeping for a second
        t.sleep(1)

        #Read database if irrigation has been done and if so, then make sure the minutes number is reset to 0
        nighti = dbfetch('NIGHT_IRRIGATED','weather_settings')
        dayi = dbfetch('DAY_IRRIGATED','weather_settings')
        if nighti == 1:
            dbupdate('NIGHT_SECONDS','weather_settings','0')
            dolog("Updating NIGHT_SECONDS to value 0 in database in analyzer.py")
    
        if dayi == 1:
            dbupdate('DAY_EXTRA','weather_settings','0')
            dolog("Updating DAY_EXTRA to value 0 in database in analyzer.py")
        
        #Sleeping for a second
        t.sleep(1)
    
        #Set a baseline for temperature, with adjustments depending on humidity and pressure, then make sure each run of this script adds to a starting 0 minutes of night irrigation until it runs. During a full 24h this will build up to around 100 times the 15 minute number.

        nirrigationtime = getseconds(temp_average,humid_average,press_average)
        dolog("Has received night irrigation time in analyzer.py")
        
        #Sleeping for a second
        t.sleep(1)

        #Get the current database irrigation seconds value
        current_seconds = dbfetch('NIGHT_SECONDS','weather_settings')
        dolog("Has received current night seconds from database in analyzer.py")
        
        #Sleeping for a second
        t.sleep(1)

        #Update the current seconds value with the additonal seconds from the getseconds function
        nirriupdated = nirrigationtime + current_seconds
        dolog("Has calculated new night irrigation time in analyzer.py")
        
        #Sleeping for a second
        t.sleep(1)
    
        #Rounding off any decimals
        nirriupdated = round(nirriupdated,1)
    
        #Changing value to string for use in sql query
        nirriupdated = str(nirriupdated)

        #Update database with new night time irrigation value - For some reason, this doesn't work?
        db = MySQLdb.connect("localhost”,”user”,”pass”,”weather")
        cursor = db.cursor()
        sql = "UPDATE weather_settings SET NIGHT_SECONDS = "+nirriupdated
        try:
            cursor.execute(sql)
            db.commit()
        
        except:
            db.rollback()
        cursor.close()
        db.close()
        dolog("Has finished updating database with new NIGHT_SECONDS in analyzer.py")
        
        #Sleeping for a second
        t.sleep(1)
        
        #Checking to see what time it is for the following pressurecompare functions
        now = datetime.now()
        now_time = now.time()
        
        if now_time >= time(10,00) and now_time < time(16,00):
            addextra = pressurecompare()
            dolog("Has compared pressure from analyzer.py")
        
            #Sleeping for a second
            t.sleep(1)

            #Checking if pressurecompare found that pressure is at least 1% higher today and if so increasing DAY_EXTRA
            if addextra == 1:
                dolog("Seems pressure is 1% higher now than 24 hours ago so we're increasing DAY_EXTRA with 2 seconds in analyzer.py")
                daycurrent = dbfetch('DAY_EXTRA','weather_settings')
                dayupdated = daycurrent + 2
                dbupdate('DAY_EXTRA','weather_settings',dayupdated)
                
        #Updating the weather settings in database according to weather data
        write_weather()


        #Sleep for ~14 minutes
        t.sleep(843)
    
except KeyboardInterrupt:
    pass
    t.sleep(1)
    print(" ")
    print("Aborting analyzer script due to keyboard interrupt")