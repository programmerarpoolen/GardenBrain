# GardenBrain
Raspberry Pi program for smart garden irrigation using Sense HAT and a 1-channel relay, with a web dashboard interface

This project runs on a Raspberry Pi3 with LAMP server and Chromium web browser installed.

It should be run from the pi users home catalog in a folder called GardenBrain.

Autostart is set for the weather.py file and for starting the Chromium browser in fullscreen kiosk mode. See file Autostart Settings.txt for instructions.

The purpose of the project is to power an irrigation pump through the systems relay. The time for powering the relay each day/night depends on the weather during the day and comparison with the day before.
