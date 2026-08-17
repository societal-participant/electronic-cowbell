# Electronic Cowbell
This repository contains project files and links to parts for a 3D-printed electronic cowbell that I created. 

## About the Cowbell
The electronic cowbell is an ordinary cowbell, except that it makes noise electronically instead of like a simple metal cowbell. Simply turn on the switch, give it a gentle shake, and listen to it respond to your movement like a real cowbell.

It's a wholly unnecessary object to have, but I thought it'd be fun to take something that wasn't electronic and then make it so.

### Required Parts
The following parts are needed to assemble the electronic cowbell:

 - [Adafruit RP2040 Prop-Maker Feather with I2S Audio Amplifier](https://www.adafruit.com/product/5768)
 - [Breadboard-friendly SPDT Slide Switch](https://www.adafruit.com/product/805)
 - [Mini Oval Speaker - 8 Ohm 1 Watt](https://www.adafruit.com/product/3923)
 - [Lithium Ion Polymer Battery with Short Cable - 3.7V 420mAh](https://www.adafruit.com/product/4236)
 - Two 22 gauge wires 
 - [Double-sided foam tape](https://www.amazon.com/dp/B0DJLR75H9)
 - [3D-printed electronic cowbell enclosure](https://www.thingiverse.com/thing:7390052)

## Installing the Cowbell Files
To download the cowbell files, do the following:
 1. On the [main github page](https://github.com/societal-participant/electronic-cowbell), click the **Code** button.
 2. Click **Download ZIP**. This downloads all the project files needed.

To install the cowbell files on your `CIRCUITPY` device, do the following:
 1. Extract the ZIP file you downloaded previously.
 2. In the extracted ZIP, open the **Cowbell_app** folder.
 3. Copy the contents of the **Cowbell_app** folder to the root of your `CIRCUITPY` device. 

## Configuring the Cowbell

### Configuring Motion Settings
Changing the configuration of the motion settings is not necessary and should be done at your own risk. Make a backup of the code.py file before you change the values in case you need to revert the changes.

To change the motion settings, update the value for **MOVEMENT_THRESHOLD**. Increasing the value increases the threshold required for the  sound to play. Increase the value to increase the amount of movement necessary before the sound is played. To lower the threshold, lower the value. 


## Printing the Cowbell
The following print settings are recommended:

 - Infill 100%
 - Tree supports 

The cowbell model has standoffs inside for attaching the Feather, which is the reason supports are needed.

## Assembling the Cowbell
Assembling the cowbell is done in two parts. First, attach the peripherals to the Feather. Then, attach the Feather and the peripherals to the inside of the cowbell.

The following diagram shows where to solder or attach specific parts:
![enter image description here](https://substack-post-media.s3.amazonaws.com/public/images/18aa8d9d-e1a2-4151-bf21-c45ee63a3752_1496x1150.jpeg)

### Soldering the On/Off Switch
You attach the power switch by soldering two wires from the switch to the Feather. To attach the power switch:

1.  Cut off one of the side pins on the power switch (not the middle pin). You should be left with one side pin and the middle pin.
2.  Solder one wire to each pin.
3.  Solder the other ends of the wire to the Feather.
    1.  Solder one wire to the Ground (G) pin.
    2.  Solder the other wire to the Enable pin (EN).
4.  Double-check that the wires are properly soldered.

### Attaching the Speaker
The speaker is attached to the Feather board by using the screw terminals.

1.  Cut the male connector off of the end of the speaker wire.
2.  Unscrew the + and - screw terminals.
3.  Gently strip the ends of the two speaker wires.
4.  Place the red wire in the + terminal and the black wire in the - terminal.
5.  Screw the terminal shut.

### Attaching the Battery
Attach the battery by plugging it in to the battery terminal on the Feather.

### Attaching Everything to the Cowbell
To attach everything to the inside of the cowbell:

 1. Cut 4 small squares of double-sided foam tape.
 2. Place a square in each corner on the back of the Feather.
 3. Peel the protective paper off and stick the Feather to the standoffs inside the cowbell, making sure that the USB-C port is facing the cowbell opening.
 4. Cut small pieces of foam tape for the battery and for the on/off switch.
 5. Place a piece of foam tape on the battery and the on/off switch.
 6. Peel the protective paper off and stick the battery and the on/off switch to the inside of the cowbell. 

## Using the Cowbell

### Turning It On 
To turn on the cowbell, simply change the switch from off to on.

### Ringing The Cowbell
To ring the cowbell, while it's on, give it a gentle shake.

### Charging the Cowbell
The Feather has a USB-C charging port attached that you can use to charge the cowbell when its battery is low. Simply plug in a USB-C cable to charge it back up. 

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbNTAwNjE1NjQyLC0xMTY4NjI4MTYzLDcyOD
Q3NzYzMywtMzQ2ODAyMDc2LDE3ODMwNzMwMDAsLTY5MTMxNDk3
NCwxOTM5MjQ3OTk0LDE3NTM5MDg2MTYsLTE4MjkyMjUwNzMsLT
E1ODU2OTE5NzMsMTEwNjk3MDE0MSwtNDYxNjE0MzI1LDg4OTY5
NTIwNywxMDQyODEzMzMwLC0xMDA2ODk3NTMwLC0xMjAyMjY0Mj
gsMTYyNzU3MDgxNV19
-->