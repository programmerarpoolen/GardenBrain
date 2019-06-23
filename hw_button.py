#!/usr/bin/python

# Import required Python libraries
from sense_hat import SenseHat
import MySQLdb
import RPi.GPIO as GPIO
import time
from functions import dbfetch,dbupdate

try:

    while True:

        # We will be using the BCM GPIO numbering
        GPIO.setmode(GPIO.BCM)

        # Selecting which GPIO to target
        GPIO_CONTROL_BUTTON = 5
    
        # Set CONTROL to OUTPUT mode
        GPIO.setup(GPIO_CONTROL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        #Checking current relay status
        current_state = dbfetch('IRRIGATE_NOW','weather_settings')
    
        if GPIO.input(GPIO_CONTROL_BUTTON) == GPIO.HIGH:
        
            if current_state == 3:
            
                #Stopping relay
                
                dbupdate('IRRIGATE_NOW','weather_settings','2')
            
                #Resetting the state of the GPIO
                GPIO.setup(GPIO_CONTROL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            elif current_state == 0:
                
                #Starting relay
                
                dbupdate('IRRIGATE_NOW','weather_settings','1')
            
                #Resetting the state of the GPIO
                GPIO.setup(GPIO_CONTROL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        #Sleeping for a 0.5 second
        time.sleep(0.5)
        
        #Cleanup
        GPIO.cleanup()
    
    

except KeyboardInterrupt:
    pass
    time.sleep(1)
    print(" ")
    print("Aborting test script due to keyboard interrupt")

