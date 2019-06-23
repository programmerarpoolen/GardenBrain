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
        
            print("Button has been pressed")
        
            if current_state == 3:
            
                print("Stopping relay")
                
                dbupdate('IRRIGATE_NOW','weather_settings','2')
            
                #Resetting the state of the GPIO
                GPIO.setup(GPIO_CONTROL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            elif current_state == 0:
            
                print("Starting relay")
                
                dbupdate('IRRIGATE_NOW','weather_settings','1')
            
                #Resetting the state of the GPIO
                GPIO.setup(GPIO_CONTROL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
        else:
        
            print("Button has not been pressed")
        
        #Sleeping for a 0.2 second
        time.sleep(0.2)
        
        #Cleanup
        GPIO.cleanup()
    
    

except KeyboardInterrupt:
    pass
    time.sleep(1)
    print(" ")
    print("Aborting test script due to keyboard interrupt")

