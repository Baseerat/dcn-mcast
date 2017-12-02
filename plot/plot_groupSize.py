#!/usr/bin/python
import random
import matplotlib.pyplot as plt
from utils import *
#random.seed(0)

def randomSample(N, method, _min):
    size = 0
    if method == 'tri': # triangular distribution
        size = int(random.triangular(_min-1, N+3, _min+4))%N+1
    elif method == 'beta': # beta distribution
        size = int((N-_min+1)*random.betavariate(0.6, 0.6))+_min
    elif method == 'norm_r': # reverse norm distribution
        p = random.gauss(0.5,0.25)
        if p < 0.5: p = abs(0.5-p)
        else: p = abs(1.5-p)
        size = int(N*p)%N+1
    elif method == 'expo': # exponential distribution
        size = int(random.expovariate(0.12))%N+1
    elif method == 'expo_r': # reverse exponential distribution
        size = N-int(random.expovariate(0.12))%N
    elif method == 'gamma': # gamma distribution
        size = int(random.gammavariate(2.5,2)*N/15+_min-1)%N+1
    elif method == 'gamma': # gamma distribution
        size = int(random.gammavariate(2.5,2)*N/15+_min-1)%N+1
    elif method == 'mix1':
        seed = random.random()
        if seed < 0.1:
            size = random.randint(_min,N)
        else:
            size = int(random.gammavariate(2.5,0.5)*N/15+_min-1)%N+1
    elif method == 'mix2':
        r = random.random()
        if r < 0.01:
            size = N-int(random.gammavariate(1,0.1)*N/15)%N
        else:
            size = int(random.gammavariate(1.4,0.1)*N/15+_min-1)%N+1
    elif method == 'mix3':
        r = random.random()
        if r < 0.02:
            size = N-int(random.gammavariate(1,0.1)*N/15)%N
        else:
            size = int(random.gammavariate(2,0.2)*N/15+_min-1)%N+1
    elif method == 'mix4':
        r = random.random()
        if r < 0.02:
            size = N-int(random.gammavariate(1,0.1)*N/15)%N
        elif r >= 0.02 and r < 0.42:
            size = random.randint(_min, N)
        else:
            size = int(random.gammavariate(2,0.2)*N/15+_min-1)%N+1
    else: # uniform distribution
        size = random.randint(_min,N)
    size = max(size, _min)
    return size

UserNum = 1000
GroupNum = 100000
groupSize = [0]*GroupNum

for i in range(GroupNum):
    groupSize[i] = randomSample(UserNum, 'mix3', 4)

plt.figure(0)
ccdf_groupSize = CDF(groupSize, 1000)

plt.figure(1)

ax1 = plt.subplot(211)
#plt.title('Histogram of group size distribution')
plt.hist(groupSize, bins = UserNum-3)
#plt.xlabel('number of hosts per group')
plt.ylabel('frequency')
plt.grid('on')
plt.yticks([])

ax2 = plt.subplot(212, sharex=ax1)
#plt.title('CCDF of group size distribution')
p1, = plt.plot(ccdf_groupSize[0], ccdf_groupSize[1])
label1 = StatLabel(groupSize)
plt.legend([p1], [label1], bbox_to_anchor=(1,0), loc=4, prop={'size':10})
plt.xlabel('number of hosts per group')
#plt.xscale('log')
#plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')

plt.setp(ax1.get_xticklabels(), visible=False)

plt.figure(2)
p1, = plt.plot(ccdf_groupSize[0], ccdf_groupSize[1])
label1 = StatLabel(groupSize)
plt.legend([p1], [label1], bbox_to_anchor=(1,0), loc=4, prop={'size':10})
plt.xlabel('number of hosts per group')
plt.xscale('log')
#plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')

plt.show()
