# Occupancy
2015-2016 senior design. 

Occupancy is a system of sensors that can be spread across a building and be analyzed, in our case we are designing it for a college library. These sensory units will be used in order to establish the number of people in each area, and the amount of time they spend in each area. This information can then be used in order to make the library more convenient for students. 

#CO2 Grid-EYE
This code is used on a Tiva Launchpad with a CO2 sensor and a Grid-EYE. The CO2 sensor picks up the amount of CO2 in each area which can be used to establish the amount of people within the area and we can establish the air quality of it. The Grid-EYE is an 8x8 grid of tempurature, and from a top down veiw we can use this in order to establish the number of people in a ten foot area. 

#Occupancy-Testing
Occupancy test v1.1 is the first iteration of having the system 'working.' The central unit sends a remote at command request via it's xbee to the sensor nodes xbee. This raises a pin on the xbee which activates a pin interrupt on the launchpad, which leads to the launchpad reading the data from the sensors, then sending this data back over the xbee to the central unit. See RPi serial format for packet structure

#PCB 
The .brd and .sch files were created using Eagle CS for the Occupancy project. These files will be converted into Gerber files to be sent to a professional fabricator. 
