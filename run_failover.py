#!/usr/bin/python
import random
from network import *
from multicast import *

k = 48
n = 64
r = 9
pa = 3
pb = 3
C = 1000 # multicast capacity
N = 30000 # group number

network = ABFatTree(k)
distribution = AddressDistribution(k, n, r, pa, pb)
#tenants = Tenants_x(network, 80, 1000,'c')
tenants = Tenants_(network, 3000, 10, 5000, 'r')

failed_switchess = set()
switches =set()
for p in range(k):
    for a in range(k/2):
        switches.add('A%d.%d'%(p,a))

M = 4
T = 10
failed_switches = [0]*M
for i in range(M):
    failed_switches[i] = []
for i in range(T):
    failed_switches[0].append(set(random.sample(switches, 10)))
    failed_switches[1].append(set(random.sample(switches, 50)))
    failed_switches[2].append(set(random.sample(switches, 100)))
    failed_switches[3].append(set(random.sample(switches, 200)))


G = Groups(k, n, N, tenants, network)

route = [0]*M
stretch = [0]*M
unreachable = [0]*M
unreachable_r = [0]*M
for j in range(M):
    route[j] = []
    stretch[j] = []
    unreachable[j] = []
    unreachable_r[j] = []

for i in range(N):
    if i%1000 == 0:
        print 'compute stretch for group %d'%i
    for j in range(M):
        for t in range(T):
            route[j].append(multicast_failover(G.groups[i], network, distribution, failed_switches[j][t], pa, pb))


for i in range(N):
    for j in range(M):
        if route[j][i][0] > 0:
            stretch[j].append(route[j][i][0])
        unreachable_r[j].append(route[j][i][1])
        unreachable[j].append(route[j][i][2])

outFile = open('plot/output/failover.py', 'w')
outFile.write('stretch = ' + str(stretch) + '\n\n' \
                  + 'unreachable_r = ' + str(unreachable_r) + '\n\n' \
                  + 'unreachable = ' + str(unreachable))

