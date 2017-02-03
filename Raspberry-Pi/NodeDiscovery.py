# --------------------------------------------------------------------------------------------- #
#                                                                                               #
#   University of North Texas                                                                   #
#   Department of Electrical Engineering                                                        #
#                                                                                               #
#   Faculty Advisors:   Dr. Xinrong Li, Dr. Jesse Hamner                                        #
#   Name:               Ovie Onoriose                                                           #
#                                                                                               #
#   Date:               01/29/2017                                                              #
#                                                                                               #
#   Title:              XBee node discovery script		                                        #
#   Version:            1.1                                                                     #
#                                                                                               #
#   Description:                                                                                #
#       This script pings other xbees located on the network and displays the lower 8 			#
#		bytes of their serial addresses. This code snippet is incorporated in other files		#
#		in this project.																		#
#                                                                                               #
#   Dependencies:                                                                               #
#       Python3.5.1, Pyserial					                                                #
#                                                                                               #
#   Change Log:                                                                                 #
#                                                                                               #
# --------------------------------------------------------------------------------------------- #



import serial
import time

ser = serial.Serial('COM5', 115200, timeout=5)  # open serial port


class MyList(list):
    def __repr__(self):
        return '[' + ', '.join("0x%X" % x if type(x) is int else repr(x) for x in self) + ']'


def discovery():
    # reset serial buffers
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # send out broadcast requesting serials of all nodes on network
    node_request = (0x7E, 0x0, 0xF, 0x17, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xFF, 0xFF, 0xFF, 0xFE, 0x2, 0x73,
                    0x6C, 0xB)
    ser.write(node_request)
    time.sleep(0.25)
    # received packets from nodes should be 23 bytes each
    nodes = int(ser.in_waiting / 23)
    if nodes == 0:
        print('No nodes found')

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
        node_address = data[14:18]
        node_list.append((i, node_address))

node = ''
node_list = []
discovery()
for i in node_list:
    node = str(MyList(i[1]))
#    print(MyList(i[1]))
    print(node)
