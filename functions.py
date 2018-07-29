#!/usr/bin/python

# Import required Python libraries
from datetime import datetime, time, timedelta
import MySQLdb
import RPi.GPIO as GPIO
import time
import subprocess
import sys
import logging
import os
import json
    
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
        
        # Sleeping for a second
        time.sleep(1)

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
    if avtemp >= 4.0 and avtemp <= 10.0:
        basetime = 0.5
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
        basetime = 1.0
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
        basetime = 1.5
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
        basetime = 1.9
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
        basetime = 2.2
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
        basetime = 2.4
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
        basetime = 2.5
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
        basetime = 2.6
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
        basetime = 2.8
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
    pressure = fetched[3]
    
    # Setting current weather depending on weather data
    if humidity > 50 and pressure < 995 or humidity > 85:
        current = 0
        logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GardenBrain/events.log', level=logging.INFO)
        logging.info('Functions.py - Writing weather as Rainy')
    elif humidity < 40 and pressure > 1005 or humidity < 30:
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
