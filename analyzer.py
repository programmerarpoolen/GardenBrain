#!/usr/bin/python

# Import required Python libraries
from datetime import datetime, time
import time as t
import MySQLdb
from functions import dbfetch,dbupdate,minutedata,averager,getseconds,dolog,pressurecompare,write_weather
import json
        
#Sleeping for 2 seconds
t.sleep(2)

#Loading the JSON config file
config = json.loads(open('/var/www/html/config.json').read())

try:

    #This script should be on a loop running once every 15 minutes or so
    while True:

        #Start with collecting the data for the last 15 minutes
        temperature = minutedata('TEMPERATURE')
        humidity = minutedata('HUMIDITY')
        pressure = minutedata('PRESSURE')
        dolog("Analyzer.py - Weather data received from database")
        
        #Sleeping for a second
        t.sleep(1)

        #Get the average temperature, humidity and pressure for those 15 minutes
        temp_average = averager(temperature)
        humid_average = averager(humidity)
        press_average = averager(pressure)
        dolog("Analyzer.py - Weather data averaged")
        
        #Sleeping for a second
        t.sleep(1)

        #Read database if irrigation has been done and if so, then make sure the minutes number is reset to 0
        nighti = dbfetch('NIGHT_IRRIGATED','weather_settings')
        dayi = dbfetch('DAY_IRRIGATED','weather_settings')
        if nighti == 1:
            dbupdate('NIGHT_SECONDS','weather_settings','0')
            dolog("Analyzer.py - Updating NIGHT_SECONDS to value 0 in database")
    
        if dayi == 1:
            dbupdate('DAY_EXTRA','weather_settings','0')
            dolog("Analyzer.py - Updating DAY_EXTRA to value 0 in database")
        
        #Sleeping for a second
        t.sleep(1)
    
        #Set a baseline for temperature, with adjustments depending on humidity and pressure, then make sure each run of this script adds to a starting 0 minutes of night irrigation until it runs. During a full 24h this will build up to around 100 times the 15 minute number.

        nirrigationtime = getseconds(temp_average,humid_average,press_average)
        dolog("Analyzer.py - Has received night irrigation time")
        
        #Sleeping for a second
        t.sleep(1)

        #Get the current database irrigation seconds value
        current_seconds = dbfetch('NIGHT_SECONDS','weather_settings')
        dolog("Analyzer.py - Has received current night seconds from database")
        
        #Sleeping for a second
        t.sleep(1)

        #Update the current seconds value with the additonal seconds from the getseconds function
        nirriupdated = nirrigationtime + current_seconds
        dolog("Analyzer.py - Has calculated new night irrigation time")
        
        #Sleeping for a second
        t.sleep(1)
    
        #Rounding off any decimals
        nirriupdated = round(nirriupdated,1)
    
        #Changing value to string for use in sql query
        nirriupdated = str(nirriupdated)

        #Update database with new night time irrigation value - For some reason, this doesn't work?
        db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
        cursor = db.cursor()
        sql = "UPDATE weather_settings SET NIGHT_SECONDS = "+nirriupdated
        try:
            cursor.execute(sql)
            db.commit()
        
        except:
            db.rollback()
        cursor.close()
        db.close()
        dolog("Analyzer.py - Has finished updating database with new NIGHT_SECONDS")
        
        #Sleeping for a second
        t.sleep(1)
        
        #Checking to see what time it is for the following pressurecompare functions
        now = datetime.now()
        now_time = now.time()
        
        if now_time >= time(10,00) and now_time < time(16,00):
            addextra = pressurecompare()
            dolog("Analyzer.py - Has compared pressure")
        
            #Sleeping for a second
            t.sleep(1)
            
            #Checking weather and temperature, and increasing daytime irrigation if it's sunny and hot
            currentweather = dbfetch('WEATHERNOW','weather_settings')
            daycurrent = dbfetch('DAY_EXTRA','weather_settings')
            dayupdated = 0
            if currentweather == 3 and temp_average > 35:
                dayupdated = daycurrent + 5
                dolog("Analyzer.py - Today it's sunny and hot so we're increasing DAY_EXTRA with 5 seconds")
            elif currentweather == 3 and temp_average > 30:
                dayupdated = daycurrent + 4
                dolog("Analyzer.py - Today it's sunny and hot so we're increasing DAY_EXTRA with 4 seconds")
            elif currentweather == 3 and temp_average > 25:
                dayupdated = daycurrent + 2
                dolog("Analyzer.py - Today it's sunny and hot so we're increasing DAY_EXTRA with 2 seconds")
            elif currentweather == 3 and temp_average > 20:
                dayupdated = daycurrent + 1
                dolog("Analyzer.py - Today it's sunny and hot so we're increasing DAY_EXTRA with 1 second")
        
            #Sleeping for a second
            t.sleep(1)

            #Checking if pressurecompare found that pressure is at least 1% higher today and if so increasing DAY_EXTRA
            if addextra == 1:
                dolog("Analyzer.py - Pressure is 1% higher now than 24 hours ago so we're increasing DAY_EXTRA with 2 seconds")
                if dayupdated > daycurrent:
                    dayupdated = dayupdated + 2
                else:
                    dayupdated = daycurrent + 2
            
            #Updating DAY_EXTRA in the database with new value
            if dayupdated > daycurrent:
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
