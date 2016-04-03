# Occupancy
2015-2016 senior design. 

Occupancy is a system of sensors that can be spread across a building and be analyzed, in our case we are designing it for a college library. These sensory units will be used in order to establish the number of people in each area, and the amount of time they spend in each area. This information can then be used in order to make the library more convenient for students. 

#CO2 Grid-EYE
This code is used on a Tiva Launchpad with a CO2 sensor and a Grid-EYE. The CO2 sensor picks up the amount of CO2 in each area which can be used to establish the amount of people within the area and we can establish the air quality of it. The Grid-EYE is an 8x8 grid of tempurature, and from a top down veiw we can use this in order to establish the number of people in a ten foot area. 

#XbeeComs
This code creates a dummy grideye packet and periodically sends an API packet containing this data to the coordinator on the Xbee network.

#XbeeComs V1-3
This code replaces the timer interrupt of XbeeComs with a Pin interrupt so the sensor unit will only send data when it's requested.
