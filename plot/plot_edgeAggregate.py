#!/usr/bin/python
import matplotlib.pyplot as plt
from utils import *
from output.aggregateEdges import *
from output.out import links as links_c, switches as switches_c, groupSize as groupSize_c

coreLinks_c = []
podLinks_c = []
edgeLinks_c = []
coreSwitches_c = []
aggrSwitches_c = []
edgeSwitches_c = []

for link in links_c.keys():
    if link.find('C') == 0:
        coreLinks_c.append(links_c[link])
    elif link.find('A') == 0:
        podLinks_c.append(links_c[link])
    elif link.find('E') == 0:
        edgeLinks_c.append(links_c[link])
    else:
        print link

for switch in switches_c.keys():
    if switch.find('C') == 0:
        coreSwitches_c.append(switches_c[switch])
    if switch.find('A') == 0:
        aggrSwitches_c.append(switches_c[switch])
    if switch.find('E') == 0:
        edgeSwitches_c.append(switches_c[switch])

plt.figure(0)
ccdf_hosts_c = CCDF(groupSize_c['members'], 1000)
ccdf_pods_c  = CCDF(groupSize_c['pods'], 1000)
ccdf_edges_c = CCDF(groupSize_c['edges'], 1000)
ccdf_addr_core_c = CCDF(coreSwitches_c, 1000)
ccdf_addr_aggr_c = CCDF(aggrSwitches_c, 1000)
ccdf_addr_edge_c = CCDF(edgeSwitches_c, 1000)
ccdf_link_core_c = CCDF(coreLinks_c, 100)
ccdf_link_aggr_c = CCDF(podLinks_c, 1000)
ccdf_link_edge_c = CCDF(edgeLinks_c, 1000)
ccdf_addr_edge_aggr = CCDF(switches[1], 1000)
ccdf_link_edge_aggr = CCDF(links[1],1000)
'''
plt.figure(1)
plt.suptitle('CCDF of group size and distribution')
plt.subplot(311)
p1, = plt.plot(ccdf_hosts_c[0], ccdf_hosts_c[1])
label1 = 'collocate '+StatLabel(groupSize_c['members'])
plt.legend([p1], [label1], bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of hosts per group')
plt.xscale('log')
plt.ylim(0,1)
plt.grid('on')

plt.subplot(312)
p1, = plt.plot(ccdf_pods_c[0], ccdf_pods_c[1])
label1 = 'collocate '+StatLabel(groupSize_c['pods'])
plt.legend([p1], [label1], bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of pods per group')
plt.ylim(0,1)
plt.grid('on')

plt.subplot(313)
p1, = plt.plot(ccdf_edges_c[0], ccdf_edges_c[1])
label1 = 'collocate '+StatLabel(groupSize_c['edges'])
plt.legend([p1], [label1], bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of edge switches per pod per group')
plt.ylim(0,1)
plt.grid('on')
'''

plt.figure(2)
#plt.suptitle('CCDF of multicast addresses on switches\n dashed -> after aggregation ')
#ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_addr_core_c[0], ccdf_addr_core_c[1], 'b-')
p2, = plt.plot(ccdf_addr_aggr_c[0], ccdf_addr_aggr_c[1], 'g-')
p3, = plt.plot(ccdf_addr_edge_c[0], ccdf_addr_edge_c[1], 'r-')
p4, = plt.plot(ccdf_addr_edge_aggr[0], ccdf_addr_edge_aggr[1], 'r--')
label1 = 'core '+StatLabel(coreSwitches_c)
label2 = 'aggr '+StatLabel(aggrSwitches_c)
label3 = 'edge '+StatLabel(edgeSwitches_c)
label4 = 'edge '+StatLabel(switches[1])
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of group addresses on a switch')
plt.ylim(0,1)
plt.grid('on')
'''
ax2 = plt.subplot(212, sharex=ax1)
#p1, = plt.plot(ccdf_addr_core_c[0], ccdf_addr_core_c[1], 'b-')
#p2, = plt.plot(ccdf_addr_aggr_c[0], ccdf_addr_aggr_c[1], 'g-')
p3, = plt.plot(ccdf_addr_edge_c[0], ccdf_addr_edge_c[1], 'r-')
p4, = plt.plot(ccdf_addr_edge_aggr[0], ccdf_addr_edge_aggr[1], 'r--')
plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')

plt.setp(ax1.get_xticklabels(), visible=False)
'''
plt.figure(3)
#plt.suptitle('CCDF of traffic rate on links\n dashed -> after aggregation')
'''
ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_link_core_c[0], ccdf_link_core_c[1], 'b-')
p2, = plt.plot(ccdf_link_aggr_c[0], ccdf_link_aggr_c[1], 'g-')
p3, = plt.plot(ccdf_link_edge_c[0], ccdf_link_edge_c[1], 'r-')
p4, = plt.plot(ccdf_link_edge_aggr[0], ccdf_link_edge_aggr[1], 'r--')
label1 = 'core-aggr '+StatLabel(coreLinks_c)
label2 = 'aggr-edge '+StatLabel(podLinks_c)
label3 = 'edge-host '+StatLabel(edgeLinks_c)
label4 = 'edge-host '+StatLabel(links[1])
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.ylim(0,1)
plt.grid('on')
'''
#ax2 = plt.subplot(212, sharex=ax1)
p1, = plt.plot(ccdf_link_core_c[0], ccdf_link_core_c[1], 'b-')
p2, = plt.plot(ccdf_link_aggr_c[0], ccdf_link_aggr_c[1], 'g-')
p3, = plt.plot(ccdf_link_edge_c[0], ccdf_link_edge_c[1], 'r-')
p4, = plt.plot(ccdf_link_edge_aggr[0], ccdf_link_edge_aggr[1], 'r--')
label1 = 'core-aggr '+StatLabel(coreLinks_c)
label2 = 'aggr-edge '+StatLabel(podLinks_c)
label3 = 'edge-host '+StatLabel(edgeLinks_c)
label4 = 'edge-host '+StatLabel(links[1])
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('traffic rate on a link')
plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')

#plt.setp(ax1.get_xticklabels(), visible=False)

plt.show()
