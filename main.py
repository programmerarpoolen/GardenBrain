#!/usr/bin/python

# Import required Python libraries
import time as t
import subprocess
from datetime import datetime, time
from functions import dbfetch,dbupdate,weather_cleanup,dolog,sysstart

#Writing system start time to database for showing uptime in the Dashboard
sysstart()
        
#Sleeping for a second
t.sleep(1)

#Declaring variable relay_proc
relay_proc = None

try:

    #Time checking loop that starts irrigation at set times
    while True:
    
        #Checking to see what time it is and starts the subprocess if it should
        now = datetime.now()
        now_time = now.time()
        nirrigated = dbfetch('NIGHT_IRRIGATED','weather_settings')
        dirrigated = dbfetch('DAY_IRRIGATED','weather_settings')
    
        if now_time >= time(01,00) and now_time < time(02,00):
            #Start subprocess if irrigation hasn't been done yet
            if nirrigated == 0:
                print("Time for some irrigation!")
                try:
                    # Old part that was buggy
                    # p = subprocess.Popen(['/home/pi/GardenBrain/relay.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    
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
                    # Old part that was buggy
                    # p = subprocess.Popen(['/home/pi/GardenBrain/relay.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    
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

except KeyboardInterrupt:
    pass
    t.sleep(1)
    print(" ")
    print("Aborting main script due to keyboard interrupt")
