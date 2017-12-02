#!/usr/bin/python
import matplotlib.pyplot as plt
from utils import *
from output.failover import *

plt.rc('pdf',fonttype = 42)
plt.rc('ps',fonttype = 42)

M = 4

plt.figure(0)
ccdf_stretch = [0]*M
ccdf_unreachable = [0]*M
ccdf_unreachable_r = [0]*M
for i in range(M):
    ccdf_stretch[i] = CCDF(stretch[i], 1000)
    ccdf_unreachable[i] = CCDF(unreachable[i], 1000)
    ccdf_unreachable_r[i] = CCDF(unreachable_r[i], 1000)

plt.figure(1)
ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_stretch[0][0], ccdf_stretch[0][1], '-*')
p1.set_markevery(200)
p2, = plt.plot(ccdf_stretch[1][0], ccdf_stretch[1][1], '-o')
p2.set_markevery(200)
p3, = plt.plot(ccdf_stretch[2][0], ccdf_stretch[2][1], '-^')
p3.set_markevery(200)
p4, = plt.plot(ccdf_stretch[3][0], ccdf_stretch[3][1], '-s')
p4.set_markevery(200)
label1 = '10 failures'
label2 = '50 failures'
label3 = '100 failures'
label4 = '200 failures'
l = plt.legend([p4,p3,p2,p1], [label4, label3, label2, label1], \
                      bbox_to_anchor=(1,1), loc=1, prop={'size':9}, numpoints=1, markerscale=0.8)
l.set_frame_on(False)
plt.yscale('log')
plt.ylabel('CCDF', size=11)
plt.xlabel('Average route stretch of a multicast group',size=11)
plt.xlim(1,2)
plt.ylim(0.000001,1)
plt.tick_params(labelsize=11)
ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey')
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey')

ax2 = plt.subplot(212)
p1, = plt.plot(ccdf_unreachable_r[0][0], ccdf_unreachable_r[0][1], '-*')
p1.set_markevery(200)
p2, = plt.plot(ccdf_unreachable_r[1][0], ccdf_unreachable_r[1][1], '-o')
p2.set_markevery(200)
p3, = plt.plot(ccdf_unreachable_r[2][0], ccdf_unreachable_r[2][1], '-^')
p3.set_markevery(200)
p4, = plt.plot(ccdf_unreachable_r[3][0], ccdf_unreachable_r[3][1], '-s')
p4.set_markevery(200)
label1 = '10 failures'
label2 = '50 failures'
label3 = '100 failures'
label4 = '200 failures'
l = plt.legend([p4,p3], [label4, label3], \
                      bbox_to_anchor=(1,1), loc=1, prop={'size':9}, numpoints=1, markerscale=0.8)
l.set_frame_on(False)
plt.yscale('log')
plt.ylabel('CCDF',size=11)
plt.xlabel('Unreachable hosts of a multicast group',size=11)
plt.xlim(0,1)
#plt.ylim(0,1)
plt.tick_params(labelsize=11)
#plt.xticks([0,0.1,0.2,0.3,0.4,0.5], ['0','10%','20%','30%','40%','50%'])
plt.xticks([0,0.2,0.4,0.6,0.8,1], ['0','20%','40%','60%','80%','100%'])
ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey')
ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey')

plt.show()
