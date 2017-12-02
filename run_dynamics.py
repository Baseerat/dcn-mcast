#!/usr/bin/python
from network import *
from multicast import *
import matplotlib.pyplot as plt

def mean(array):
    return sum(array)/float(len(array))

def median(array):
    values = sorted(array)
    if len(values) % 2 == 1:
        return values[(len(values)+1)/2-1]
    else:
        lower = values[len(values)/2-1]
        upper = values[len(values)/2]
        return (float(lower + upper)) / 2


#linkFile = open('trace/links.py', 'w')
#switchFile = open('trace/switches.py', 'w')
#groupFile = open('trace/groupSize.py', 'w')

k = 48
n = 64
r = 9
pa = 3
pb = 3
c = 2000 # multicast capacity
N = 10000 # group number

network = ABFatTree(k)
distribution = AddressDistribution(k, n, r, pa, pb)
tenants = Tenants_x(network, 80, 1000,'random')
#tenants = Tenants(network, 300, 100, 5000, 'random')

G = Groups(k, n, N, tenants, network)
groupSize = {}
groupSize['pods'] = [0]*N
groupSize['edges'] = []
groupSize['members'] = [0]*N
for i in range(N):
    groupSize['pods'][i] = len(G.groups[i].members.keys())
    for pod in G.groups[i].members.keys():
        groupSize['edges'].append(len(G.groups[i].members[pod].keys()))
    groupSize['members'][i] = G.groups[i].size

'''
index = 2
#print tenants[219]
print ''
print 'id:    ', G.groups[index].id
print 'block: ', G.groups[index].block
print 'rate:  ', G.groups[index].rate
print 'tenant:', G.groups[index].tenant
print 'member:', G.groups[index].members
print 'hosts: ', G.groups[index].hosts
print 'size:  ', G.groups[index].size
'''

update = {}
update['cores_J'] = []
update['aggrs_J'] = []
update['cores_L'] = []
update['aggrs_L'] = []

M = 200
updates = [0]*N
for i in range(N):
    if i%10 == 0:
        print 'dynamic %d'%i

    updates[i]={}
    updates[i]['cores_J'] = 0
    updates[i]['aggrs_J'] = 0
    updates[i]['edges_J'] = 0
    updates[i]['cores_L'] = 0
    updates[i]['aggrs_L'] = 0
    updates[i]['edges_L'] = 0

    for j in range(M):
        Dynamic(G.groups[i], tenants, network, updates[i])

    update['cores_J'].append(updates[i]['cores_J']/float(updates[i]['edges_J']))
    update['aggrs_J'].append(updates[i]['aggrs_J']/float(updates[i]['edges_J']))
    update['cores_L'].append(updates[i]['cores_L']/float(updates[i]['edges_L']))
    update['aggrs_L'].append(updates[i]['aggrs_L']/float(updates[i]['edges_L']))

updateFile = open('plot/updates.py', 'w')
updateFile.write('updates = '+str(update))
    
print mean(update['cores_J'])
print mean(update['aggrs_J'])
print mean(update['cores_L'])
print mean(update['aggrs_L'])

'''
tenantsLen = []
total = 0
print len(tenants)
for i in range(len(tenants)):
    tenantsLen.append(len(tenants[i]))
    total += len(tenants[i])
    #print '----'
    print len(tenants[i])
    #print tenants[i]
print total

#tenantsGroup = [0]*len(tenants)
#for i in range(N):
#    tenantsGroup[G.groups[i].tenant] += 1

#print tenantsGroup
plt.hist(tenantsLen,50)
plt.suptitle('Example of tenant size distribution of setting 1&2')
plt.xlabel('number of hosts per tenant (median = %.1f, mean = %.1f)'%(median(tenantsLen),mean(tenantsLen)))
plt.ylabel('number of tenants')
plt.show()

Trees = [0]*N
for i in range(N):
    if i%1000 == 0:
        print 'create tree %d'%i
    Trees[i] = multicastTree_simple(G.groups[i], network, distribution)

linkFile.write('links = '+str(network.links))
switchFile.write('switches = '+str(network.switches))
groupFile.write('groupSize = '+str(groupSize))
'''
