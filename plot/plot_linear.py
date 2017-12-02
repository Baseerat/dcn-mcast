#!/usr/bin/python
import matplotlib.pyplot as plt
from utils import *

plt.rc('pdf',fonttype = 42)
plt.rc('ps',fonttype = 42)

capacity = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000]

collocate_wve_la = [10.1, 51, 101, 198, 305, 390, 505, 602]
collocate_rand_la = [10.4, 49, 100, 190, 298, 399, 501, 607]
spread_wve_la = [3.2, 16.5, 31, 65, 97, 128, 157, 195]
spread_rand_la = [0.95, 1.9, 9.8, 19, 28.7, 37, 47.1, 56]

collocate_wve = [3.07, 16.1, 31, 62, 87, 122.2, 153.8, 184]
collocate_rand = [1.54, 7.7, 15.6, 32, 47, 62, 78, 94]
spread_wve = [2.3, 4.6, 23.8, 47.7, 71, 95.2, 117, 142]
spread_rand = [0.4, 1.97, 3.94, 7.9, 11.8, 15.6, 20.1, 23.6]

plt.figure(1)
ax1 = plt.subplot(111)
p1, = plt.plot(capacity, collocate_wve_la, '-o', color='blue')
p2, = plt.plot(capacity, collocate_wve, '-.o', color='blue')
p1.set_markeredgecolor('blue')
p1.set_markerfacecolor('white')
p2.set_markeredgecolor('blue')
p2.set_markerfacecolor('white')
p3, = plt.plot(capacity, collocate_rand_la, '-^', color='red')
p4, = plt.plot(capacity, collocate_rand, '-.^', color='red')
p3.set_markeredgecolor('red')
p3.set_markerfacecolor('white')
p4.set_markeredgecolor('red')
p4.set_markerfacecolor('white')
p5, = plt.plot(capacity, spread_wve_la, '-s', color='green')
p6, = plt.plot(capacity, spread_wve, '-.s', color='green')
p5.set_markeredgecolor('green')
p5.set_markerfacecolor('white')
p6.set_markeredgecolor('green')
p6.set_markerfacecolor('white')
p7, = plt.plot(capacity, spread_rand_la, '-*', color='black')
p8, = plt.plot(capacity, spread_rand, '-.*', color='black')
label1 = 'Near, WVE, la'
label2 = 'Near, WVE'
label3 = 'Near, U, la'
label4 = 'Near, U'
label5 = 'Rand, WVE, la'
label6 = 'Rand, WVE'
label7 = 'Rand, U, la'
label8 = 'Rand, U'
l1 = plt.legend([p3,p4,p7,p8], \
               [label3, label4, label7, label8], \
               bbox_to_anchor=(0,1), loc=2, prop={'size':9}, numpoints=1, markerscale=0.8)
l1.set_frame_on(False)
l2 = plt.legend([p1,p2,p5,p6], \
               [label1, label2, label5, label6], \
               bbox_to_anchor=(1,1), loc=1, prop={'size':9}, numpoints=1, markerscale=0.8)
l2.set_frame_on(False)
plt.gca().add_artist(l1) # add l1 as a separate artist to the axes
plt.tick_params(labelsize=11)
plt.xlabel('Multicast address capacity on a switch', size=11)
plt.ylabel('Number of groups',size=11)
plt.xlim(0,6300)
plt.ylim(-10,320)
plt.yticks(range(0,301,50),[0,'50K','100K','150K','200K','250K','300K'], size=11)
plt.show()
