#!/usr/bin/python

# Import required Python libraries
from datetime import datetime, time, timedelta, date
import MySQLdb
import RPi.GPIO as GPIO
import time
import subprocess
import sys
import logging
import os
import json
from astral import Astral
from shutil import copyfile
    
#This function logs anything to the project events.log file
def dolog(message):
    logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
    logging.info(message)
    return

#This function connects to database and returns the first value from the selected table and column
def dbfetch(dbcolumn,dbtable):
    try:
        config = json.loads(open('/var/www/html/config.json').read())
        db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
        cursor = db.cursor()
        sql = "select "+dbcolumn+" from "+dbtable
        cursor.execute(sql)
        global delay
        fetched = cursor.fetchone()
        data = float(fetched[0])
        cursor.close()
        db.close()
        return data;
        
    except:
        print("Database connection failed")

#This function connects to database and updates the value in the selected column in the selected table to the set new value
def dbupdate(dbcolumn,dbtable,newvalue):
    try:
        config = json.loads(open('/var/www/html/config.json').read())
        db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
        cursor = db.cursor()
        sql = "UPDATE "+dbtable+" SET "+dbcolumn+" = %s"
        try:
            cursor.execute(sql,(newvalue))
            db.commit()
        
        except:
            db.rollback()
        cursor.close()
        db.close()
        return
    except:
        print("Database connection failed")
        
#This function connects to database and drops the selected table if it exists
def dbdroptable(dbtable):
    try:
        config = json.loads(open('/var/www/html/config.json').read())
        db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
        cursor = db.cursor()
        sql = "DROP TABLE IF EXISTS "+dbtable
        cursor.execute(sql)
        cursor.close()
        db.close()
        return
    except:
        print("Database connection failed")

#This function connects to database to create new tables for weather_settings    
def dbcreatewstables():
    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql = """CREATE TABLE weather_settings (NIGHT_SECONDS DECIMAL(5,2),DAY_EXTRA DECIMAL(5,2), NIGHT_IRRIGATED INT, DAY_IRRIGATED INT, UPTIME DATETIME, IRRIGATE_NOW INT, WEATHERNOW INT, REBOOTNOW INT, MANSTART DATETIME)"""
    try:
        cursor.execute(sql)
        db.commit()
        
    except:
        db.rollback()
    cursor.close()
    db.close()
    return

#This function connects to database to create new tables for weather_data    
def dbcreatewdtables():
    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql = """CREATE TABLE weather_data (DATETIME DATETIME,TEMPERATURE DECIMAL(4,1),HUMIDITY DECIMAL(4,1),PRESSURE DECIMAL(5,1))"""
    try:
        cursor.execute(sql)
        db.commit()
        
    except:
        db.rollback()
    cursor.close()
    db.close()
    return

#This function connects to database to write initial values to the weather_settings table        
def db_ws_insert(ns,de,ni,di,ut,ir,wn,rn,ms):
    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql = "INSERT INTO weather_settings VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql,(ns,de,ni,di,ut,ir,wn,rn,ms))
        db.commit()
        
    except:
        db.rollback()
    cursor.close()
    db.close()
    return

#This function connects to database to write values to the weather_data table        
def db_wd_insert(time,temp,humidity,pressure):
    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql = "INSERT INTO weather_settings VALUES (%s,%s,%s,%s)"
    try:
        cursor.execute(sql,(time,temp,humidity,pressure))
        db.commit()
        
    except:
        db.rollback()
    cursor.close()
    db.close()
    return

#This function switches on the relay for a set period of time, and then shuts it off again
def relay_delay(wait_time):
    
    # Sleeping for a second
    time.sleep(1)

    print("Relay control function")
    
    # We will be using the BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)

    # Selecting which GPIO to target
    GPIO_CONTROL = 6

    # Set CONTROL to OUTPUT mode
    GPIO.setup(GPIO_CONTROL, GPIO.OUT)
    
    # Starting the relay
    GPIO.output(GPIO_CONTROL, True)
    
    # Sleeping for set amount of time
    try:
        time.sleep(wait_time)
    except:
        time.sleep(60)
        print("Setting delay failed, using default 60 seconds")
    
    # Stopping the relay
    GPIO.output(GPIO_CONTROL, False)
    
    # Cleanup
    GPIO.cleanup()

#This function switches on the relay on or off and expects the argument 'on' or 'off'
def relay_manual(action):

    # Selecting which GPIO to target
    GPIO_CONTROL = 6
    
    if action == "on":
        
        # Sleeping for a 0.1 seconds
        time.sleep(0.1)

        # We will be using the BCM GPIO numbering
        GPIO.setmode(GPIO.BCM)

        # Set CONTROL to OUTPUT mode
        GPIO.setup(GPIO_CONTROL, GPIO.OUT)
    
        #Starting the relay
        GPIO.output(GPIO_CONTROL, True)
    
        #Logging the event
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Relay has been switched on')
        
    elif action == "off":
        
        try:
            #Stopping the relay
            GPIO.output(GPIO_CONTROL, False)
            
        except:
            # We will be using the BCM GPIO numbering
            GPIO.setmode(GPIO.BCM)

            # Set CONTROL to OUTPUT mode
            GPIO.setup(GPIO_CONTROL, GPIO.OUT)
    
            #Starting the relay
            GPIO.output(GPIO_CONTROL, False)
    
        #Logging the event
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Relay has been switched off')
    
        #Cleanup
        GPIO.cleanup()
    
#This function gets the last 15 minutes for any column in the weather_data table
def minutedata(dbcolumn):
    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql = "SELECT "+dbcolumn+" FROM weather_data WHERE DATETIME > NOW() - INTERVAL 15 MINUTE"
    cursor.execute(sql)
    fetched = cursor.fetchall()
    cursor.close()
    db.close()
    return fetched; #Returns a tuple
    
#This function removes all weather data older than 12 months
def weather_cleanup():
    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql = "DELETE FROM weather_data WHERE DATETIME < NOW() - INTERVAL 1 YEAR"
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return
    
#This function finds the average in a tuple, as from the minutedata function
def averager(incoming):
    datasummary = 0
    itemsnumber = 0
    for i in incoming:
        datasummary = datasummary + i[0]
        itemsnumber = itemsnumber + 1
    try:
        dataaverage = datasummary / itemsnumber
    except:
        dataaverage = 0
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - ZeroDivisionError occured in averager function, returning a 0')
    return dataaverage

#This function takes incoming average temperature, humidity, and pressure and returns how many seconds to add to irrigation
def getseconds(avtemp,avhum,avpress):
    basetime = 0.0
    
    #If temperature is between 4 - 10 degrees
    if avtemp >= -5 and avtemp <= 3.9:
        basetime = 0.1
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between -5 and 4 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.05
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.01
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.01
    
    #If temperature is between 4 - 10 degrees
    elif avtemp >= 4.0 and avtemp <= 10.0:
        basetime = 0.3
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 4 and 10 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.2
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.1
    
    #If temperature is between 10 - 14 degrees
    elif avtemp >= 10.1 and avtemp <= 14.0:
        basetime = 0.9
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 10 and 14 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.2
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.1
    
    #If temperature is between 14 - 18 degrees
    elif avtemp >= 14.1 and avtemp <= 18.0:
        basetime = 1.4
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 14 and 18 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.2
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.1
    
    #If temperature is between 18 - 22 degrees
    elif avtemp >= 18.1 and avtemp <= 22.0:
        basetime = 1.8
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 18 and 22 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.2
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.1
    
    #If temperature is between 22 - 25 degrees
    elif avtemp >= 22.1 and avtemp <= 25.0:
        basetime = 2.4
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 22 and 25 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.2
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.1
    
    #If temperature is between 25 - 28 degrees
    elif avtemp >= 25.1 and avtemp <= 28.0:
        basetime = 2.6
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 25 and 28 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.3
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.2
    
    #If temperature is between 28 - 31 degrees
    elif avtemp >= 28.1 and avtemp <= 31.0:
        basetime = 2.9
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 28 and 31 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.3
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.2
    
    #If temperature is between 31 - 34 degrees
    elif avtemp >= 31.1 and avtemp <= 34.0:
        basetime = 3.2
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is between 31 and 34 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.3
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.2
    
    #If temperature over 34 degrees
    elif avtemp >= 34.1:
        basetime = 3.5
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Temperature is over 34 degrees')
        
        #If humidity is over 50 %
        if avhum >= 50:
            basetime = basetime - 0.4
        
        #If pressure is under 995
        if avpress < 995:
            basetime = basetime - 0.1
        
        #If pressure is over 1005
        if avpress > 1005:
            basetime = basetime + 0.2
    
    #Rounding the number to one decimal
    basetime = round(basetime,1)
    
    return basetime;

#This function compares air pressure now with air pressuse yesterday the same time
def pressurecompare():
    config = json.loads(open('/var/www/html/config.json').read())
    # SQL Query for getting data for 24 hours previously is SELECT PRESSURE FROM `weather_data` WHERE DATETIME >= NOW() - INTERVAL 1 DAY ORDER BY `DATETIME` ASC LIMIT 1
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql1 = "SELECT PRESSURE FROM weather_data WHERE DATETIME >= NOW() - INTERVAL 1 DAY ORDER BY DATETIME ASC LIMIT 1"
    cursor.execute(sql1)
    fetched = cursor.fetchone()
    oldpressure = float(fetched[0])
    
    # SQL Query for getting most recent data is SELECT PRESSURE FROM `weather_data` ORDER BY `DATETIME` DESC LIMIT 1
    sql2 = "SELECT PRESSURE FROM weather_data ORDER BY DATETIME DESC LIMIT 1"
    cursor.execute(sql2)
    fetched = cursor.fetchone()
    newpressure = float(fetched[0])
    
    cursor.close()
    db.close()
    
    compared = newpressure/oldpressure
    
    if compared >= 1.01:
        data = 1
    else:
        data = 0
    
    return data;
    
#This function reboots the system if one or more scripts has stopped running
def sysreboot():
    
    print('Rebooting the system!')
    
    logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
    logging.info('Functions.py - Rebooting the system')
    
    os.system('sudo reboot')
        
    return;

#This function saves system start date to database
def sysstart():
    
    startup = time.strftime("%Y-%m-%d %H:%M")
    
    startup = str(startup)
    
    print("Writing system startup-time to database: "),startup
    
    try:
        config = json.loads(open('/var/www/html/config.json').read())
        db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
        cursor = db.cursor()
        sql = "UPDATE weather_settings SET UPTIME = '"+startup+"'"
        try:
            cursor.execute(sql)
            db.commit()
        
        except:
            db.rollback()
        cursor.close()
        db.close()
        return;
    except:
        print("Database connection failed")

#This function gets sun related data for a set location
def sundata():

    #This code uses the Astral library (which needs to be installed together with the dependency Pytz) to get sun related data for a set location, such as sunrise and sunset.
    
    config = json.loads(open('/var/www/html/config.json').read())

    now = datetime.now()
    now_time = now.time()

    print ('\nTime now is %s \n' % now_time)

    city_name = config['location']['city']

    a = Astral()

    a.solar_depression = 'civil'

    city = a[city_name]

    print('Information for %s/%s\n' % (city_name, city.region))

    timezone = city.timezone

    print('Timezone: %s' % timezone)

    print('Latitude: %.02f; Longitude: %.02f\n' % \
    (city.latitude, city.longitude))

    today = datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d')

    sun = city.sun(date=datetime.date(today), local=True)

    dawn = str(sun['dawn'])[11:-6]
    dawn = datetime.strptime(dawn, '%H:%M:%S').time()
    sunrise = str(sun['sunrise'])[11:-6]
    sunrise = datetime.strptime(sunrise, '%H:%M:%S').time()
    noon = str(sun['noon'])[11:-6]
    noon = datetime.strptime(noon, '%H:%M:%S').time()
    sunset = str(sun['sunset'])[11:-6]
    sunset = datetime.strptime(sunset, '%H:%M:%S').time()
    dusk = str(sun['dusk'])[11:-6]
    dusk = datetime.strptime(dusk, '%H:%M:%S').time()

    print('Dawn:    %s' % dawn)
    print('Sunrise: %s' % sunrise)
    print('Noon:    %s' % noon)
    print('Sunset:  %s' % sunset)
    print('Dusk:    %s \n' % dusk)

    if now_time > dawn:
        print ('Time is after dawn')
    else:
        print ('Time is before dawn')

    if now_time > sunrise:
        print ('Time is after sunrise')
    else:
        print ('Time is before sunrise')

    if now_time > noon:
        print ('Time is after noon')
    else:
        print ('Time is before noon')

    if now_time > sunset:
        print ('Time is after sunset')
    else:
        print ('Time is before sunset')

    if now_time > dusk:
        print ('Time is after dusk\n')
    else:
        print ('Time is before dusk\n')
        
    if sunset > now_time and now_time > sunrise:
        current = "day"
        total = datetime.combine(date.today(), sunset) - datetime.combine(date.today(), sunrise)
        total = total.total_seconds()
        print('The following is the time in seconds in a day %s\n' % total)
        actual = datetime.combine(date.today(), now_time) - datetime.combine(date.today(), sunrise)
        actual = actual.total_seconds()
        percentage = actual / total * 100
        percentage = round(percentage, 2)
        print('We have passed %s percent of the day\n' % percentage)
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - It is daytime and %s percent of the day has passed' % percentage)
    else:
        current = "night"
        total1 = datetime.combine(date.today(), datetime.strptime('23:59:59', '%H:%M:%S').time()) - datetime.combine(date.today(), sunset)
        total2 = datetime.combine(date.today(), sunrise) - datetime.combine(date.today(), datetime.strptime('00:00:00', '%H:%M:%S').time())
        total = total1.total_seconds() + total2.total_seconds()
        print('The following is the time in seconds in a night %s\n' % total)
        if now_time > sunset and now_time < datetime.strptime('23:59:59', '%H:%M:%S').time():
            actual = datetime.combine(date.today(), now_time) - datetime.combine(date.today(), sunset)
            actual = actual.total_seconds()
            percentage = actual / total * 100
            percentage = round(percentage, 2)
            print('We have passed %s percent of the night\n' % percentage)
        else:
            previous_evening = datetime.combine(date.today(), datetime.strptime('23:59:59', '%H:%M:%S').time()) - datetime.combine(date.today(), sunset)
            from_midnight = datetime.combine(date.today(), now_time) - datetime.combine(date.today(), datetime.strptime('00:00:00', '%H:%M:%S').time())
            previous_evening = previous_evening.total_seconds()
            from_midnight = from_midnight.total_seconds()
            actual = previous_evening + from_midnight
            percentage = actual / total * 100
            percentage = round(percentage, 2)
            print('We have passed %s percent of the night\n' % percentage)
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - It is night time and %s percent of the night has passed' % percentage)
        
    return current, percentage

#This function saves the current weather to database. 0 = Rain, 1 = Cloudy, 2 = Sun and clouds, 3 = Sunny
def write_weather():
    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
        
    # Fetching data from database, sorted by the latest entry
    sql1 = "SELECT * from weather_data ORDER BY DATETIME DESC"
    try:
        cursor.execute(sql1)
        fetched = cursor.fetchone()
        
    except:
        db.rollback()
        
    # This sets usable variables in the correct format
    temperature = fetched[1]
    humidity = fetched[2]
    humidity = float(humidity)
    pressure = fetched[3]
    
    # This returns day or night, and how much of the day or night that has passed in percentage
    time_of_day = sundata()
    
    # Modifying the humidity data, depending on time of day, since it's way more humid in the night time regardless if it's raining or not
    if time_of_day[0] == "day":
        if time_of_day[1] > 75 and time_of_day[1] < 99:
            humidity = humidity * 0.85
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.85')
        elif time_of_day[1] > 65 and time_of_day[1] < 75:
            humidity = humidity * 0.9
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.9')
        elif time_of_day[1] > 55 and time_of_day[1] < 65:
            humidity = humidity * 0.95
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.95')
        elif time_of_day[1] > 45 and time_of_day[1] < 55:
            humidity = humidity * 1
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 1')
        elif time_of_day[1] > 35 and time_of_day[1] < 45:
            humidity = humidity * 0.95
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.95')
        elif time_of_day[1] > 25 and time_of_day[1] < 35:
            humidity = humidity * 0.9
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.9')
        elif time_of_day[1] > 1 and time_of_day[1] < 25:
            humidity = humidity * 0.85
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.85')
    else:
        if time_of_day[1] > 75 and time_of_day[1] < 99:
            humidity = humidity * 0.75
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.75')
        elif time_of_day[1] > 65 and time_of_day[1] < 75:
            humidity = humidity * 0.65
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.65')
        elif time_of_day[1] > 55 and time_of_day[1] < 65:
            humidity = humidity * 0.55
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.55')
        elif time_of_day[1] > 45 and time_of_day[1] < 55:
            humidity = humidity * 0.5
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.5')
        elif time_of_day[1] > 35 and time_of_day[1] < 45:
            humidity = humidity * 0.55
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.55')
        elif time_of_day[1] > 25 and time_of_day[1] < 35:
            humidity = humidity * 0.65
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.65')
        elif time_of_day[1] > 1 and time_of_day[1] < 25:
            humidity = humidity * 0.75
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Functions.py - Multiplying humidity by 0.75')
    
    # Setting current weather depending on weather data
    if humidity > 50 and pressure < 995 or humidity > 85:
        current = 0
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Writing weather as Rainy')
    elif humidity < 40 and pressure > 1005 or humidity < 30 or pressure > 1015 and humidity < 60:
        current = 3
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Writing weather as Sunny')
    elif humidity < 50 and pressure < 995 or humidity > 60:
        current = 1
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Writing weather as Cloudy')
    else:
        current = 2
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Writing weather as Sunny and Cloudy')
        
    # Making it a string
    current = str(current)
        
    # Updating the database with the current weather
    sql2 = "UPDATE weather_settings SET WEATHERNOW = "+current
    try:
        cursor.execute(sql2)
        db.commit()
        
    except:
        db.rollback()
        
    cursor.close()
    db.close()
    return;
        
#This function opens a script from the program folder if it's not running already
def keepopen(process_name):

    tmp = os.popen("ps -Af").read()

    if process_name not in tmp[:]:
        subprocess.Popen(['/home/pi/GardenBrain/'+process_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("The script is not running. Starting the script now.")
    else:
        print("The script is already running.")
    return;
    
#This function returns the time in seconds between started manual irrigation and now
def mandiff():

    config = json.loads(open('/var/www/html/config.json').read())
    db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
    cursor = db.cursor()
    sql = "select MANTIME from weather_settings"
    cursor.execute(sql)
    global delay
    fetched = cursor.fetchone()
    dbtime = fetched[0]
    cursor.close()
    db.close()
    print("Current db time is: ",dbtime)
    print("")
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
    nowtime = datetime.strptime(nowtime,"%Y-%m-%d %H:%M:%S")
    print("Current time is: ",nowtime)
    print("")
    difference = nowtime - dbtime
    difference = difference.total_seconds()
    print("The difference is: ",difference)
    print("")
    return difference;
    
#This function returns the last few lines in the logfile to see what services has been run (incomplete)
def lastlogs():
    lines = 50
    fname = '/home/pi/GardenBrain/events.log'
    bufsize = 8192
    fsize = os.stat(fname).st_size
    iter = 0
    with open(fname) as f:
        if bufsize > fsize:
            bufsize = fsize-1
            data = []
            while True:
                iter +=1
                f.seek(fsize-bufsize*iter)
                data.extend(f.readlines())
                if len(data) >= lines or f.tell() == 0:
                    print(''.join(data[-lines:]))
                    break

#This function moves the current logs out of the main log file and saves it to daily log files instead, keeping one per day of the week (7 days in total)
def logsave():
    basefile = '/home/pi/GardenBrain/events.log'
    thismoment = datetime.now()
    weekday = thismoment.strftime("%A")
    weekday = weekday.lower()
    newfile = '/home/pi/GardenBrain/%s.log' % weekday
    copyfile(basefile, newfile)
    os.system('rm -f %s' % basefile)
    
#This function recalculates the temperature reading with respect to enclosure and sensor placement
def tempcorrection(temperature):
    
    temp = round(temperature, 1)
    
    #Getting the CPU temperature for corrections
    board_temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
    array = board_temp.split("=")
    array2 = array[1].split("'")
    cpu_temp = array2[0]
    
    #Correcting the temperature using the CPU temperature and a factor (default 5.466) and printing the value
    temp = temp - ((float(cpu_temp) - temp)/5.466)
    temp = round(temp, 1)
    
    if temp > -5 and temp < 4:
        temp = temp - 9
    elif temp >= 4 and temp < 10:
        temp = temp - 7
    elif temp >= 10 and temp < 14:
        temp = temp - 7
    elif temp >= 14 and temp < 18:
        temp = temp - 7
    elif temp >= 18 and temp < 22:
        temp = temp - 7
    elif temp >= 22 and temp < 25:
        temp = temp - 7
    elif temp >= 25 and temp < 28:
        temp = temp - 7
    elif temp >= 28 and temp < 31:
        temp = temp - 7
    elif temp >= 31 and temp < 34:
        temp = temp - 7
    else:
        temp = temp - 10
    
    return temp

#This function checks weather entries for the last 1 days to see if it was newly started from a long sleep to prevent rebooting for no irrigation time before the system has reached normal working temperature
def longsleep():
    try:
        config = json.loads(open('/var/www/html/config.json').read())
        db = MySQLdb.connect(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['dbname'] )
        cursor = db.cursor()
        sql = "SELECT *, (DATE(NOW()) - INTERVAL 1 DAY) AS diff FROM `weather_data` WHERE DATETIME >= (DATE(NOW()) - INTERVAL 1 DAY)"
        cursor.execute(sql)
        global delay
        fetched = cursor.fetchall()
        cursor.close()
        db.close()
        if len(fetched) > 2000:
            just_woke = False
            #Logging the event
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Main.py - System has not recently woken up from long sleep')
        else:
            just_woke = True
            #Logging the event
            logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
            logging.info('Main.py - System has recently woken up from long sleep')
            
        return just_woke; #Returns True or False
    
    except:
        print("Database connection failed")