# --------------------------------------------------------------------------------------------- #
#                                                                                               #
#   University of North Texas                                                                   #
#   Department of Electrical Engineering                                                        #
#                                                                                               #
#   Faculty Advisors:   Dr. Xinrong Li, Dr. Jesse Hamner                                        #
#   Name:               Ovie Onoriose                                                           #
#                                                                                               #
#   Date:               02/02/2017                                                              #
#                                                                                               #
#   Title:              Grideye Animator for SQlite datbase                                     #
#   Version:            1.1                                                                     #
#                                                                                               #
#   Description:                                                                                #
#       This script retrieves grideye data from a local sqlite database and creates             #
#       an animation from that data. The user can specify the dates that they would             #
#       like to gather data between as well as the frame rate of the produced animation         #
#                                                                                               #
#   Dependencies:                                                                               #
#       Python3.5.1, Numpy, Matplotlib, sqlite3                                                 #
#                                                                                               #
#   Change Log:                                                                                 #
#                                                                                               #
# --------------------------------------------------------------------------------------------- #

import numpy as np
from matplotlib import pyplot as plt
import sqlite3

start = '2017-01-21'
end = '2017-01-23'
fps = 5

#connect to database and fetch data
conn = sqlite3.connect('occupancy.db')  # connect to the database
c = conn.cursor()
##c.execute('SELECT Grideye FROM data WHERE Datetime BETWEEN "2017-01-15" AND "2017-01-17"')
##grideye_data = c.fetchall()
##c.execute('SELECT Datetime FROM data WHERE Datetime BETWEEN "2017-01-15" AND "2017-01-17"')
##datetime_data = c.fetchall()
c.execute('SELECT Grideye FROM data WHERE Datetime BETWEEN "{}" AND "{}"'.format(start, end))
grideye_data = c.fetchall()
c.execute('SELECT Datetime FROM data WHERE Datetime BETWEEN "{}" AND "{}"'.format(start, end))
datetime_data = c.fetchall()

#convert string from sql database to list
for idx, x in enumerate(grideye_data):
    grideye_data[idx]=[float(i) for i in grideye_data[idx][0].split(',') if i != '0']
    
for idx, x in enumerate(datetime_data):
    datetime_data[idx]= x[0]

gridata = np.array(grideye_data).reshape((len(grideye_data),8,8))

#Set up the figure
fig = plt.figure()
ax = fig.add_subplot(111)
a=np.full((8,8),20)
im = ax.imshow(a, vmin=20, vmax=30, interpolation='none',cmap = plt.get_cmap('hot'))
ttl = ax.text(.01, 1.005, '', transform = ax.transAxes)

#Set up initial frame of animation
def init():
    im.set_data(np.full((8,8),20))
    ttl.set_text('')
    return [im, ttl]

#set up frames afterwards
def animate(i):
    im.set_data(gridata[i])
    ttl.set_text('Frame: {}\nTime: {}'.format(i, datetime_data[i]))
    return [im, ttl]

plt.rcParams['animation.ffmpeg_path'] = 'c:\\ffmpeg\\bin\\ffmpeg.exe'

from matplotlib import animation #for some reason a warning is thrown if this is declared before plt.rcParams

anim = animation.FuncAnimation(fig, animate, init_func = init, frames = len(gridata), blit = False)
anim.save('basic_animation.mp4', fps=fps)
plt.show(block=False)
