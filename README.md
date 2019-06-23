# GardenBrain

Raspberry Pi program for smart garden irrigation using Sense HAT, a 1-channel relay and a 7" touchscreen, with a web dashboard interface.

This project runs on a Raspberry Pi3 with LAMP server and Chromium web browser installed.

It should be run from the pi users home catalog in a folder called GardenBrain.

Autostart is set for the weather.py file and for starting the Chromium browser in fullscreen kiosk mode. See file Autostart Settings.txt for instructions.

The purpose of the project is to power an irrigation pump through the systems relay. The time for powering the relay each day/night depends on the weather during the day and comparison with the day before. It irrigates between 1-2 am, and again between 4-5 pm if needed.
In my garden, it powers a submersible pump that pumps water to a 1/4" drip irrigation system on my balcony to around 50 different plants. The amount of water each plant gets are regulated with different flow rate drip nozzles.

Irrigation can be started manually as well though the dashboard, where the Pi can be rebooted as well.

This is a work in pregress though and the web interface does need work and it would be nice if the user could click the graphs for humidity and pressure to move that graph and data up and switch place with the temperature data that is currently there. The irrigation time thresholds need to be adjusted in the functions.py file as well, to adjust your actual needs.

And this is my first ever RPi project, my first ever work in Python and PHP, I've never worked with databases myself and it's been 20 years since I took that HTML/CSS course, SO please don't hate, be kind and help out to improve the project if you can.
Cleaning the code is helping too, in case you who are reading this feels like contributing :)

Especially helpful is contributions around data usage to get weather icon correct and dashboard more useful, but also with how to best set irrigation times in the functions.py file in the getseconds function.

UPDATE: 
The project has now been updated to work without screen, and with a hardware button for toggling irrigation on/off if wanted. 
It still works with screen and web dashboard too though.
I have also uploaded a 3D design file pack containing 3D files for full enclosure, for those that need that and has a 3D printer available.
