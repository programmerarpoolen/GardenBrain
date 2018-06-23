# GardenBrain
Raspberry Pi program for smart garden irrigation using Sense HAT, a 1-channel relay and a 7" touchscreen, with a web dashboard interface.

This project runs on a Raspberry Pi3 with LAMP server and Chromium web browser installed.

It should be run from the pi users home catalog in a folder called GardenBrain.

Autostart is set for the weather.py file and for starting the Chromium browser in fullscreen kiosk mode. See file Autostart Settings.txt for instructions.

The purpose of the project is to power an irrigation pump through the systems relay. The time for powering the relay each day/night depends on the weather during the day and comparison with the day before.

This is a work in pregress though and the web interface does need work. The graphs are currently static and these need to be fixed so that they work properly. Also the irrigation time thresholds need to be adjusted in the functions.py file as well, to adjust your actual needs.

And this is my first ever RPi project, my first ever work in Python and PHP, I've never worked with databases myself and it's been 20 years since I took that HTML/CSS course, SO please don't hate, be kind and help out to improve the project if you can.
