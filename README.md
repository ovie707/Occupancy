# Occupancy Modelling using Sensor Networks
Master Thesis

A system of sensors that can be spread across a building and be analyzed, in our case we are designing it for a college library. These sensory units will be used in order to estimate the number of people in each area, and the amount of time they spend in each area. This information can then be used in order to make the library more convenient for students. 

Nodes are built around Tiva-C launchpads and communicate using Xbee Pro S2Bs. The central point consists of a Raspberry Pi and another Xbee Pro S2B

# Occupancy-test
Contains older files used during undergraduate project

#Raspberry-Pi
Contains python code used on the central Raspberry Pi
RPiOccupancyV2 requires pyserial and sqlite3 libraries

Currently, the code only requests data from one node, but it can be easily expanded to handle multiple nodes. Threading may be added in the future to make expansion easier. Need to look into it more.

#Tiva-C-Launchpad
Contains C code used on the Launchpad MCU to gather data from the sensors and send it to the Rapsberry Pi.
Occupancy-testingV1-2 uses Tivaware 2.1.2.111

Current sensors:
Panasonic Grideye, SenseAir S8 CO2 sensor, RHT03 temperature/humidity sensor

Also contains code to test Xbee API mode connection.
