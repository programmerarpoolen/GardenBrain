#!/usr/bin/python

# Import required Python libraries
from datetime import datetime, time
import MySQLdb
import RPi.GPIO as GPIO
import time
from functions import dbfetch,dbupdate,dolog,relay_manual,relay_delay,sysreboot,mandiff
import logging
        
#Sleeping for 3 seconds
time.sleep(3)

#Running a loop to check for scheduled tasks
while True:
    
    #Getting settings table from DB
    irrigatedata = dbfetch('IRRIGATE_NOW','weather_settings')
    rebootdata = dbfetch('REBOOTNOW','weather_settings')
    if irrigatedata == 3:
        difference = mandiff()
        if difference/60 > 5:
            irrigatedata = 2
        else:
            print("Time doesn't exceed 5 minutes")
    
    if irrigatedata == 1:
        dbupdate('IRRIGATE_NOW','weather_settings','3')
        print("Irrigating now")
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
        dbupdate('MANTIME','weather_settings',str(nowtime))
        relay_manual('on')
    
    if irrigatedata == 2:
        dbupdate('IRRIGATE_NOW','weather_settings','0')
        print("Stopping irrigation now")
        relay_manual('off')
        
    if rebootdata == 1:
        dbupdate('REBOOTNOW','weather_settings','0')
        time.sleep(10)
        sysreboot()
    
    #Sleeping for 5 seconds
    time.sleep(5)
