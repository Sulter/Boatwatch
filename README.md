# Boatwatch
Quick hack project for data collection from my boat, and some automatic control.

## What does it do?
* Connect to a mobile network (done)
* Read temp/humidity from dht22 data and write it to html (done)
* Graph out of data (done)
* Display camera (done)
* Dynamic dns setup (done)
* PID control of dehumidifier with relay to keep humidity below 60% (WIP)
* Add pressure sensor to measure dew point (WIP)

## Setup etc.
Runs on odroid C1+, but should run on anything that works with wiringPi.
Build the dht22 C dynamic lib using build.sh script
Then just use the rc.local and move the files so it fits
Sakis3gz needs to be compiled from source

[Sakis3g](https://github.com/Trixarian/sakis3g-source)
[dht22](https://github.com/technion/lol_dht22) (with changes for easier use)

### Requires
motion (for the webcam stream)
wiringPi (dht22)
binutils (building dht22)
python3
bs4
matplotlib/pylab
sakis3gz (usbmodem switcher/connector)

## Hardware
* dht22 data <-> Pin 7 @ 3.3V
* USBmodem 12d1:143a
* Webcam
