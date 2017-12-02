#!/usr/bin/python 
import matplotlib.pyplot as plt
from utils import *
from output.out import *

coreLinks = []
podLinks = []
edgeLinks = []
coreSwitches = []
aggrSwitches = []
edgeSwitches = []

aggrMcast = []
edgeMcast = []


distribution = ''

for link in links.keys():
    if link.find('C') == 0:
        coreLinks.append(links[link])
    elif link.find('A') == 0:
        podLinks.append(links[link])
    elif link.find('E') == 0:
        edgeLinks.append(links[link])
    else:
        print link

for switch in switches.keys():
    if switch.find('C') == 0:
        coreSwitches.append(switches[switch])
    if switch.find('A') == 0:
        aggrSwitches.append(switches[switch])
        aggrMcast.append(switches[switch]-unicast[switch])
    if switch.find('E') == 0:
        edgeSwitches.append(switches[switch])
        edgeMcast.append(switches[switch]-unicast[switch])

groupHosts = []
for host in hosts.keys():
    groupHosts.append(hosts[host])

plt.figure(0)
ccdf_hosts = CDF(groupSize['members'], 50000)
ccdf_pods  = CDF(groupSize['pods'], 1000)
ccdf_edges = CDF(groupSize['edges'], 1000)
ccdf_group_hosts = CDF(groupHosts, 1000)

ccdf_addr_core = CDF(coreSwitches, 1000)
ccdf_addr_aggr = CDF(aggrSwitches, 1000)
ccdf_addr_edge = CDF(edgeSwitches, 1000)
ccdf_addr_amcast = CDF(aggrMcast, 1000)
ccdf_addr_emcast = CDF(edgeMcast, 1000)
ccdf_link_core = CDF(coreLinks, 100)
ccdf_link_aggr = CDF(podLinks, 1000)
ccdf_link_edge = CDF(edgeLinks, 1000)


plt.figure(1)
#plt.suptitle('CDF of group size and distribution')
plt.subplots_adjust(hspace=0.5)
'''
plt.subplot(311)
p1, = plt.plot(ccdf_pods[0], ccdf_pods[1])
label1 = distribution+StatLabel(groupSize['pods'])
plt.legend([p1], [label1], bbox_to_anchor=(0,1), loc=3, prop={'size':9}, borderaxespad=0.)
plt.xlabel('number of pods per group')
plt.ylim(0,1)
plt.grid('on')
'''
plt.subplot(211)
p1, = plt.plot(ccdf_edges[0], ccdf_edges[1])
label1 = distribution+StatLabel(groupSize['edges'])
plt.legend([p1], [label1], bbox_to_anchor=(0,1), loc=3, prop={'size':9}, borderaxespad=0.)
plt.xlabel('number of edge switches per pod per group')
plt.ylim(0,1)
plt.grid('on')

plt.subplot(212)
p1, = plt.plot(ccdf_hosts[0], ccdf_hosts[1])
label1 = distribution+StatLabel(groupSize['members'])
plt.legend([p1], [label1], bbox_to_anchor=(0,1), loc=3, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of hosts per group')
plt.xscale('log')
plt.xticks([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000])
plt.ylim(0,1)
plt.grid('on')


plt.figure(2)
#plt.suptitle('CCDF of multicast addresses on switches')
#ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_addr_core[0], ccdf_addr_core[1], 'b-')
p2, = plt.plot(ccdf_addr_aggr[0], ccdf_addr_aggr[1], 'g-')
p3, = plt.plot(ccdf_addr_edge[0], ccdf_addr_edge[1], 'r-')
p4, = plt.plot(ccdf_addr_amcast[0], ccdf_addr_amcast[1], 'g--')
p5, = plt.plot(ccdf_addr_emcast[0], ccdf_addr_emcast[1], 'r--')
label1 = 'core '+StatLabel(coreSwitches)
label2 = 'aggr '+StatLabel(aggrSwitches)
label3 = 'edge '+StatLabel(edgeSwitches)
label4 = 'amcast '+StatLabel(aggrMcast)
label5 = 'emcast '+StatLabel(edgeMcast)
plt.legend([p1,p2,p3,p4,p5], [label1, label2, label3, label4, label5], \
               bbox_to_anchor=(1,0), loc=4, prop={'size':8})
plt.ylim(0,1)
plt.xlabel('number of group addresses on a switch')
plt.grid('on')
'''
ax2 = plt.subplot(212, sharex=ax1)
p1, = plt.plot(ccdf_addr_core[0], ccdf_addr_core[1], 'b-')
p2, = plt.plot(ccdf_addr_aggr[0], ccdf_addr_aggr[1], 'g-')
p3, = plt.plot(ccdf_addr_edge[0], ccdf_addr_edge[1], 'r-')
plt.xlabel('number of group addresses on a switch')
plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')
plt.setp(ax1.get_xticklabels(), visible=False)

#plt.figure(3)
#plt.suptitle('CCDF of traffic rate on links')
ax2 = plt.subplot(212)
p1, = plt.plot(ccdf_link_core[0], ccdf_link_core[1], 'b-')
p2, = plt.plot(ccdf_link_aggr[0], ccdf_link_aggr[1], 'g-')
p3, = plt.plot(ccdf_link_edge[0], ccdf_link_edge[1], 'r-')
label1 = 'core-aggr '+StatLabel(coreLinks)
label2 = 'aggr-edge '+StatLabel(podLinks)
label3 = 'edge-host '+StatLabel(edgeLinks)
plt.legend([p1,p2,p3], [label1, label2, label3], \
               bbox_to_anchor=(1,0), loc=4, prop={'size':8})
plt.ylim(0,1)
plt.xlabel('traffic rate on a link')
plt.grid('on')

ax2 = plt.subplot(212, sharex=ax1)
p1, = plt.plot(ccdf_link_core[0], ccdf_link_core[1], 'b-')
p2, = plt.plot(ccdf_link_aggr[0], ccdf_link_aggr[1], 'g-')
p3, = plt.plot(ccdf_link_edge[0], ccdf_link_edge[1], 'r-')
plt.xlabel('traffic rate on a link')
plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')
plt.setp(ax1.get_xticklabels(), visible=False)
'''
plt.show()
