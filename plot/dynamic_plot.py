#!/usr/bin/python 
import matplotlib.pyplot as plt

plt.rc('pdf',fonttype = 42)
plt.rc('ps',fonttype = 42)

size = [10, 20, 30, 40, 60, 80, 100, 120, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000];

N_join = [6.204, 4.343, 3.734, 3.499, 3.222, 3.004, 2.809, 2.631, 2.399, 2.078, \
          1.828, 1.635, 1.485, 1.37, 1.213, 1.12, 1.067, 1.037, 1.02, 1.011];

N_leave = [6.602, 4.435, 3.772, 3.514, 3.227, 3.012, 2.818, 2.645, 2.405, 2.083, \
           1.835, 1.64, 1.488, 1.372, 1.214, 1.121, 1.067, 1.037, 1.02, 1.011];

N_burst = [9.255, 7.212, 6.15, 5.515, 4.793, 4.375, 4.083, 3.859, 3.587, 3.25,  \
           2.991, 2.78, 2.605, 2.458, 2.223, 2.047, 1.91, 1.803, 1.717, 1.646];

N_batch = [3.652, 2.521, 2.017, 1.73, 1.414, 1.238, 1.118, 1.028, 0.922, 0.795, \
           0.7, 0.623, 0.561, 0.508, 0.426, 0.364, 0.316, 0.279, 0.249, 0.224];

plt.figure(1)
ax1 = plt.subplot(111)
p1, = plt.plot(size, N_join, 'o', color='blue')
p1.set_markeredgecolor('blue')
p1.set_markerfacecolor('white')
p2, = plt.plot(size, N_leave, 'x', color='red')
p3, = plt.plot(size, N_burst, '+', color='black')
p4, = plt.plot(size, N_batch, '*', color='green')
p4.set_markeredgecolor('green')
label1 = 'Next join when group size is $N$'
label2 = 'Next leave when group size is $N$'
label3 = '$N$ burst joins, w/o batch operation'
label4 = '$N$ burst joins, with batch operation'
l = plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
                      bbox_to_anchor=(1,1), loc=1, prop={'size':9}, numpoints=1, markerscale=0.8)
l.set_frame_on(False)
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey')
plt.yticks(range(0,11))
plt.xlabel('$(N)$ Number of hosts that subscribe to the group',fontsize=11)
plt.ylabel('Number of updates per event', fontsize=11)
plt.xlim(-50,1050)
plt.tick_params(labelsize=11)
plt.show()
