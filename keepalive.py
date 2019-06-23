#!/usr/bin/python

# Import required Python libraries
from functions import keepopen

try:

    keepopen('weather.py')
    keepopen('hw_button.py')

except KeyboardInterrupt:
    pass
    print(" ")
    print("Aborting keepalive script due to keyboard interrupt")

