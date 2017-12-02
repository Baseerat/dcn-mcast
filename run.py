#!/usr/bin/python
from network import *
from multicast import *
import matplotlib.pyplot as plt

def writeOutput(network, G, aggrGroupEdges):
    outFile = open('plot/output/out.py', 'w')
    outFile.write('links = ' + str(network.links)+'\n\n' \
                      + 'switches = ' + str(network.switches)+'\n\n' \
                      + 'groupSize = ' + str(G.groupSize())+'\n\n' \
                      + 'hosts = ' +str(network.hosts['groups']))
    if len(aggrGroupEdges) > 0:
        aggrFile = open('plot/output/aggregateAggrs.py', 'w')
        aggrFile.write('aggrSwitches = '+str(network.aggrs) +'\n\n' \
                           + 'aggrLinks = '+str(network.aggrlinks))

def writeTenant(network, tenants):
    tenantFile = open('plot/output/tenant.py', 'w')
    tenantFile.write('tenants = '+ str(tenants)+'\n\n' \
                         + 'hosts = '+ str(network.hosts['tenants']))

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
tenants = Tenants_(network, 500, 100, 5000, 'r')
writeTenant(network, tenants)

G = Groups(k, n, N, tenants, network)
aggrGroupEdges = doAggregate(k, G, network, distribution, C, pa, pb, 'a')
Trees = GenerateTrees(N, G, network, distribution, aggrGroupEdges)
writeOutput(network, G, aggrGroupEdges)
