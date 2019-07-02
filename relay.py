#!/usr/bin/python

# Import required Python libraries
import time as t
from datetime import datetime, time
from functions import dbfetch,dbupdate,relay_delay,relay_manual,dolog

#Checking to see what time it is for the following functions
now = datetime.now()
now_time = now.time()

#Sleeping for a moment
t.sleep(15)

#Getting data for the delay variable which determines how long the relay stays open
if now_time >= time(01,00) and now_time <= time(02,00):
    delay = dbfetch('NIGHT_SECONDS','weather_settings')
    dolog("Relay.py - NIGHT_SECONDS received from database :")
    dolog(delay)
elif now_time >= time(16,00) and now_time <= time(17,00):
    delay = dbfetch('DAY_EXTRA','weather_settings')
    dolog("Relay.py - DAY_EXTRA received from database :")
    dolog(delay)
else:
    #Setting delay to a default 60 seconds if the script is run outside of the set timeframes
    delay = 60

#If delay variable is not 0
if delay != 0:
    
    #Starting the delay
    relay_manual('on')

    #Sleeping for a moment
    t.sleep(delay)

    #Stopping the relay
    relay_manual('off')
    
    # Running the actual relay function that starts and stops the relay with a set delay inbetween
    # relay_delay(delay)
    
#Updating the table with new information about irrigation being done    
if now_time >= time(01,00) and now_time <= time(02,00):
    dbupdate('NIGHT_IRRIGATED','weather_settings','1')
    dbupdate('NIGHT_SECONDS','weather_settings','0')
    dolog("Relay.py - Resetting NIGHT_SECONDS to 0 and setting NIGHT_IRRIGATED to 1 in database")
elif now_time >= time(16,00) and now_time <= time(17,00):
    dbupdate('DAY_IRRIGATED','weather_settings','1')
    dbupdate('DAY_EXTRA','weather_settings','0')
    dolog("Relay.py - Resetting DAY_EXTRA to 0 and setting DAY_IRRIGATED to 1 in database")
