# --------------------------------------------------------------------------------------------- #
#                                                                                               #
#   University of North Texas                                                                   #
#   Department of Electrical Engineering                                                        #
#                                                                                               #
#   Faculty Advisors:   Dr. Xinrong Li, Dr. Jesse Hamner                                        #
#   Name:               Ovie Onoriose                                                           #
#                                                                                               #
#   Date:               01/22/2017                                                              #
#                                                                                               #
#   Title:              Occupancy Client for Raspberry Pi                                       #
#   Version:            6.2                                                                     #
#                                                                                               #
#   Description:                                                                                #
#       This script sends a probe request on the Xbee connected to the Raspberry Pi             #
#       to find all other active Xbee's (connected to sensor nodes) on the network              #
#       It then proceeds to send requests and store the received data from each node            #
#       sequentially. This received data is stored in a remote mySQL database                   #
#                                                                                               #
#   Dependencies:                                                                               #
#       Python 3.5.1, Pyserial, pymysql                                                         #
#                                                                                               #
#   Issues:                                                                                     #
#       The new CO2 sensors I received are different than the older ones and have a             #
#       different protocol for accessing the sensor data. I will need to update the             #
#       code to reflect the new protocol. The sensor nodes will also need to be updated         #
#       to support the new mode of CO2 sensor                                                   #
#                                                                                               #
#   Change Log:                                                                                 #
#       v6.2 (1/29/2017)                                                                        #
#           Now connecting to MySQL databse instead of local sqlite3 database. I'm using the    #
#           pymysql library instead of mysqldb because it's compatible with Python 3.5.         #
#       v6.1 (01/22/2017)                                                                       #
#           In the case that a node loses power or otherwise becomes unresponsive,              #
#           Node discovery is performed to repopulate the list of active nodes so               #
#           the program doesn't hang while trying to receive input                              #
#                                                                                               #
# --------------------------------------------------------------------------------------------- #

import serial
import pymysql
import sys
import datetime
import time
from collections import Counter
import atexit

# open serial port and connect to database
db_host = '192.168.1.125'
db_port = 3306
db_user = 'nodeuser01'
db_passwd = 'tempp@ssw0rd'
db_database = 'ovietest'
db_table = 'testdata'

try:
    conn = pymysql.connect(host = db_host,
                           port = db_port,
                           user = db_user,
                           password = db_passwd,
                           db = db_database)
    atexit.register(conn.close)
    c = conn.cursor()
    c.execute("SELECT VERSION()")
    db_version = c.fetchone()[0]
    status = '---- Connected to SQL DB ----\n\tHost: {}\n\tPort: {}\n\tDatabase: {}\n\tDatabase version : {}\n\t'.format(db_host, db_port, db_database, db_version) 

except:
    status = "ERROR - SQL DB: connection to SQLDB failed.\n\t"
    for index, msg in enumerate(sys.exc_info()):
        status += "SYS ERROR {}: {}\n\t".format(index, msg)

print(status)

ser = serial.Serial('COM5', 115200, timeout=5)  # open serial port

node_list = []

class MyList(list):
    def __repr__(self):
        return '[' + ', '.join("0x%X" % x if type(x) is int else repr(x) for x in self) + ']'


def remove_node_dupes(x):
    count = Counter((i[1]) for i in x)
    while len([i for i in x if count[(i[1])] > 1]) > 1:
        x.remove(max([i for i in x if count[(i[1])] > 1]))
        count = Counter((i[1]) for i in x)


def find_checksum(packet):  # find checksums of Xbee packets
    sum = 0
    for i in range(3,len(packet)):
        sum += packet[i]
    return (0xFF - (0xFF & sum))

def discovery():

    # reset serial buffers
    ser.flushInput()
    ser.flushOutput()
    time.sleep(.1)
    # send out broadcast requesting serials of all nodes on network
    node_request = [0x7E, 0x0, 0xF, 0x17, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xFF, 0xFF, 0xFF, 0xFE, 0x2, 0x73,
                    0x6C, 0xB] #checksum is already here
    ser.write(node_request)
    time.sleep(5)
    # received packets from nodes should be 23 bytes each
    nodes = int(ser.in_waiting/23)
    if nodes == 0:
        print('no nodes discovered')
        discovery()
        return
    del node_list[:]

    for i in range(nodes):
        a = ser.read()
        a = int.from_bytes(a, byteorder='big')
        if a != 0x7E:  # check starting bit, discarding if wrong
            discovery()
            return
        l = ser.read(2)
        l = int.from_bytes(l, byteorder='big')
        b = ser.read()
        b = int.from_bytes(b, byteorder='big')
        if b != 0x97:  # check if this is indeed a node identification packet
            discovery()
            return
        data = ser.read(l)
        node_address = tuple(data[14:18])
        node_list.append((i, node_address))
        print('node discovered. address:{0}'.format(MyList(list(node_address)),))
        remove_node_dupes(node_list)
    print('\n')

def data_request(serial_low):
    ser.flushInput()
    ser.flushOutput()
    time.sleep(.1)
    # reset pin interrupt on launchpad
    request_end = [0x7E, 0x00, 0x10, 0x17, 0x00, 0x00, 0x13, 0xA2, 0x00] + list(serial_low) + \
                  [0xFF, 0xFE, 0x02, 0x44, 0x31, 0x04]  # packet without checksum
    request_end.append(find_checksum(request_end)) # append checksum to packet
    ser.write(request_end)
    time.sleep(0.1)
    # Request for data  for testing I'm sending test, the final thing to send is currently commented
    # toggles pin interrupt
    request = [0x7E, 0x00, 0x10, 0x17, 0x00, 0x00, 0x13, 0xA2, 0x00] + list(serial_low) + \
              [0xFF, 0xFE, 0x02, 0x44, 0x31, 0x05]  # packet without checksum
    request.append(find_checksum(request))  # append checksum to packet
    ser.write(request)
    print('requesting data from {0}\n'.format(MyList(list(serial_low)),))
    return read_packet()


def read_packet():
    a = ser.read(1)
    if len(a) == 0:
        print('no data received. rediscovering nodes...\n')
        return 1  # if no data is read, return 1 (Run discovery and restart at beginning of node_list)
    elif int.from_bytes(a, byteorder='big') != 0x7E:  # check starting bit, discarding if wrong
        read_packet()
        return
    l = ser.read(2)
    l = int.from_bytes(l, byteorder='big')  # calculate length of packet
    b = ser.read(1)
    b = int.from_bytes(b, byteorder='big')
    print('data type is {0}'.format(MyList([b]),))
    if b == 0x90:
        data_store(l)
##    elif b == 0x95:
##        node_joined(l)
##        return 2  # if a new node connects, return 2 (restart at beginning of node_list w/out running discovery)
    else:
        data = ser.read(l)
        print('data not synced right\n')
        print(MyList(list(data)))
    if ser.in_waiting > 0:
        return read_packet()


def data_store(l):
    grideye = [0 for i in range(70)]
    data = ser.read(l)  # read rest of packet
    print('data received:')
    print(MyList(list(data)))

    # Break data into more manageable sections
    # sixty four source address=data[0:8]
    # sixteen source address=data[8:10]
    rf_data = data[11:l - 1]

    node = rf_data[0]
    co2 = (rf_data[1] * 200)
    humid = ((rf_data[2] << 8) | rf_data[3]) / 10
    temp = ((rf_data[4] << 8) | rf_data[5]) / 10
    pir = rf_data[6]

    for i in range(64):
        grideye[i] = (((rf_data[2 * i + 7] << 8) | rf_data[2 * i + 8]) / 4)

    # map grideye data to a string for simplicity in entering them into the database
    grid_str = ','.join(map(str, grideye))

    # finds the time
    current = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S:%f")

    # insert data into database
    try:
        statement = "INSERT INTO {}(Node, Datetime, Grideye, CO2PPM, Temperature, Humidity, PIR) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(db_table)
        c.execute(statement,(node, current, grid_str, co2, temp, humid, pir))
        conn.commit()
    except:
        status = "ERROR - SQL DB: insert failed.\n\t"
        for index, msg in enumerate(sys.exc_info()):
            status += "SYS ERROR {}: {}\n\t".format(index, msg)
        conn.rollback()
        print(status)


##def node_joined(l):
##    data = ser.read(l)
##    node_address = tuple(data[17:21])
##    node_num = (max(x[0] for x in node_list)) + 1
##    node_list.append((node_num, node_address))
##    print('node joined. address:{0}'.format(MyList(list(node_address)),))
##    remove_node_dupes(node_list)

####run once
##discovery()
##for t in range(5):
##    for i in node_list:
##        x = data_request(i[1])  # if data request returns 1, start over at discovery
##        if x:                   # if data request returns 2, start over at while loop after discovery
##            break
##        else:
##            time.sleep(.1)
##            continue
##    if x == 1:
##        break
##    else:
##        time.sleep(.1)
##        continue

##run indefinitely
while True:
    discovery()
    while True:
        for i in node_list:
            x = data_request(i[1])  # if data request returns 1, start over at discovery
            if x:                   # if data request returns 2, start over at while loop after discovery
                break
        if x == 1:
            break
        else:
            print('loop starting over\n')
            continue
