#!/usr/bin/python 
from utils import *
from output.out import *

coreS = []
aggrS = []
edgeS = []

aggrM = []
edgeM = []

for switch in switches.keys():
    if switch.find('C') == 0:
        coreS.append(switches[switch])
    if switch.find('A') == 0:
        aggrS.append(switches[switch])
        aggrM.append(switches[switch]-unicast[switch])
    if switch.find('E') == 0:
        edgeS.append(switches[switch])
        edgeM.append(switches[switch]-unicast[switch])

print 'core: ', max(coreS)
print 'aggr: ', max(aggrS), max(aggrM)
print 'edge: ', max(edgeS), max(edgeM)

