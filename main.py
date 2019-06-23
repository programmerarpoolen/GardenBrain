#!/usr/bin/python

# Import required Python libraries
import time as t
import subprocess
from datetime import datetime, time
from functions import dbfetch,dbupdate,weather_cleanup,dolog,sysstart,logsave

#Writing system start time to database for showing uptime in the Dashboard
sysstart()
        
#Sleeping for a second
t.sleep(1)

#Declaring variable relay_proc
relay_proc = None

#Declaring variable logsaved
logsaved = 0

#Setting manual push button gpio to input
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:

    #Time checking loop that starts irrigation at set times
    while True:
    
        #Checking to see what time it is and starts the subprocess if it should
        now = datetime.now()
        now_time = now.time()
        nirrigated = dbfetch('NIGHT_IRRIGATED','weather_settings')
        dirrigated = dbfetch('DAY_IRRIGATED','weather_settings')
        nirriseconds = dbfetch('NIGHT_SECONDS','weather_settings')
    
        if now_time >= time(01,00) and now_time < time(02,00):
            #Start subprocess if irrigation hasn't been done yet
            if nirrigated == 0:
                print("Time for some irrigation!")
                try:
                    
                    if relay_proc is not None and relay_proc.poll() is None:
                         print('process is already running')
                    else:
                        relay_proc = subprocess.Popen(['/home/pi/GardenBrain/relay.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        dolog("Main.py - Successfully started the relay.py script")
        
                    #Sleeping for a second
                    t.sleep(1)
    
                except:
                    print("Starting night time irrigation script failed")
                    dolog("Main.py - Starting the relay.py script failed")
    
        elif now_time >= time(16,00) and now_time < time(17,00):
            #Start subprocess if irrigation hasn't been done yet
            if dirrigated == 0:
                print("Perhaps some extra irrigation?")
                try:
                    
                    if relay_proc is not None and relay_proc.poll() is None:
                         print('process is already running')
                    else:
                        relay_proc = subprocess.Popen(['/home/pi/GardenBrain/relay.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        dolog("Main.py - Successfully started the relay.py script")
        
                    #Sleeping for a second
                    t.sleep(1)
    
                except:
                    print("Starting day time irrigation script failed")
                    dolog("Main.py - Starting the relay.py script failed")
    
        elif now_time >= time(02,00) and now_time < time(03,00) and nirrigated == 1:
            #Making sure irrigation setting is restored in db after irrigation timeframe
            dbupdate('NIGHT_IRRIGATED','weather_settings','0')
        
            #Sleeping for a second
            t.sleep(1)
        
            dolog("Main.py - Resetting data for NIGHT_IRRIGATED to 0 in database")
    
        elif now_time >= time(17,00) and now_time < time(18,00) and dirrigated == 1:
            #Making sure irrigation setting is restored in db after irrigation timeframe
            dbupdate('DAY_IRRIGATED','weather_settings','0')
        
            #Sleeping for a second
            t.sleep(1)
        
            dolog("Main.py - Resetting data for DAY_IRRIGATED to 0 in database")
    
        else:
            print("No irrigation at this point")
            dolog("Main.py - Script reached end of loop without starting irrigation, loop starts from the top again")
        
            #Sleeping for a second
            t.sleep(1)
            
            #Cleaning up any 1+ year old weather data
            weather_cleanup()
        
        #Sleeping for 15 minutes (900 seconds) before starting time checking loop again
        t.sleep(900)
            
        #If time is between 23:44 and 23:59 then we move log to day log and change the variable logsaved to 1
        if now_time > time(23,44) and now_time < time(23,59) and logsaved == 0:
            logsave()
            logsaved = 1
            dolog("Main.py - Time is between 23:44 and 23:59, so we're running the logsave function")
            
        #If time is after 00:01 then we change logsaved variable back to 0
        elif now_time > time(00,01):
            logsaved = 0
            
        #Rebooting the system if time is more than 2:30 and there's 0 seconds on night irrigation
        if now_time > time(02,30) and float(nirriseconds) < 0.5:
            dbupdate('REBOOTNOW','weather_settings','1')
            dolog("Main.py - Rebooting the system as time is after 2:30 and we still have 0 seconds of night irrigation logged")

except KeyboardInterrupt:
    pass
    t.sleep(1)
    print(" ")
    print("Aborting main script due to keyboard interrupt")