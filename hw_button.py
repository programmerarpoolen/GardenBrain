#!/usr/bin/python

# Import required Python libraries
from sense_hat import SenseHat
import MySQLdb
import RPi.GPIO as GPIO
import time
from functions import dbfetch,dbupdate

# We will be using the BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Selecting which GPIO to target
GPIO_CONTROL_BUTTON = 5

# Set CONTROL to OUTPUT mode
GPIO.setup(GPIO_CONTROL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    
    while True:
        GPIO.wait_for_edge(GPIO_CONTROL_BUTTON, GPIO.RISING)
        start = time.time()
        current_state = dbfetch('IRRIGATE_NOW','weather_settings')
        print("--> Pressed <--")
        time.sleep(0.2)
        
        while GPIO.input(GPIO_CONTROL_BUTTON) == GPIO.HIGH:
            time.sleep(0.02)
            
        length = time.time() - start
        print(length)
        
        if length > 0.4:
            
            if current_state == 3:
                
                #Stopping relay
                dbupdate('IRRIGATE_NOW','weather_settings','2')
                
            elif current_state == 0:
                
                #Starting relay
                dbupdate('IRRIGATE_NOW','weather_settings','1')
    
    

except KeyboardInterrupt:
    pass
    time.sleep(1)
    print(" ")
    print("Aborting test script due to keyboard interrupt")
    GPIO.cleanup()