#!/usr/bin/python
import random
import matplotlib.pyplot as plt
from utils import *
from output.groupsize_rand_out import groupSize as groupsize
random.seed(0)

plt.rc('pdf',fonttype = 42)
plt.rc('ps',fonttype = 42)

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

UserNum = 200
GroupNum = 3000
groupSize = [0]*GroupNum

for i in range(GroupNum):
    groupSize[i] = randomSample(UserNum, '', 5)

plt.figure(0)
groupsize = groupsize['members']
cdf_groupSize = CDF(groupSize, 10000)
ccdf_hosts = CDF(groupsize, 50000)
plt.figure(1)

ax1 = plt.subplot(211)
plt.hist(groupSize, bins = UserNum-4, normed=True, facecolor='black')
plt.ylabel('frequency',size=11)
plt.yticks([0,0.005,0.01])
#plt.ylim(0,0.01)
#p1, = plt.plot(cdf_groupSize[0], cdf_groupSize[1])
#plt.ylabel('CDF')
plt.xlabel('Group size (a sample tenant with 200 VMs)', size=11)

ax3 = plt.subplot(212)
p1, = plt.plot(ccdf_hosts[0], ccdf_hosts[1])
label1 = StatLabel(groupsize)
#plt.legend([p1], [label1], bbox_to_anchor=(1,0), loc=4, prop={'size':9})
plt.figtext(0.60, 0.18,  label1,
            backgroundcolor='white', color='black', weight='roman', size=10)
plt.xlabel('Group size (all tenants)',size=11)
plt.xscale('log')
plt.ylabel('CDF',size=11)
plt.xlim(4,10000)
plt.xticks([4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000])
#plt.yscale('log')
plt.ylim(0,1)
#plt.grid('on')
ax3.xaxis.grid(True, linestyle='-', which='major', color='lightgrey')
ax3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey')

plt.show()
