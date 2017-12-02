#!/usr/bin/python
import matplotlib.pyplot as plt
from utils import *
from output.aggregateAggrs import *
from output.out import links as links_r, switches as switches_r, groupSize as groupSize_r

coreLinks_r = []
podLinks_r = []
edgeLinks_r = []
coreSwitches_r = []
aggrSwitches_r = []
edgeSwitches_r = []

links_aggr = []
switches_aggr = []


for link in links_r.keys():
    if link.find('C') == 0:
        coreLinks_r.append(links_r[link])
    elif link.find('A') == 0:
        podLinks_r.append(links_r[link])
    elif link.find('E') == 0:
        edgeLinks_r.append(links_r[link])
    else:
        print link

for switch in switches_r.keys():
    if switch.find('C') == 0:
        coreSwitches_r.append(switches_r[switch])
    if switch.find('A') == 0:
        aggrSwitches_r.append(switches_r[switch])
    if switch.find('E') == 0:
        edgeSwitches_r.append(switches_r[switch])

for link in aggrLinks.keys():
    links_aggr.append(aggrLinks[link])

for switch in aggrSwitches.keys():
    switches_aggr.append(aggrSwitches[switch])

plt.figure(0)
ccdf_hosts_r = CCDF(groupSize_r['members'], 1000)
ccdf_pods_r  = CCDF(groupSize_r['pods'], 1000)
ccdf_edges_r = CCDF(groupSize_r['edges'], 1000)
ccdf_addr_core_r = CCDF(coreSwitches_r, 1000)
ccdf_addr_aggr_r = CCDF(aggrSwitches_r, 1000)
ccdf_addr_edge_r = CCDF(edgeSwitches_r, 1000)
ccdf_link_core_r = CCDF(coreLinks_r, 100)
ccdf_link_aggr_r = CCDF(podLinks_r, 1000)
ccdf_link_edge_r = CCDF(edgeLinks_r, 1000)
ccdf_addr_aggr_aggr = CCDF(switches_aggr, 1000)
ccdf_link_aggr_aggr = CCDF(links_aggr,1000)
'''
plt.figure(1)
plt.suptitle('CCDF of group size and distribution')
plt.subplot(411)
p1, = plt.plot(ccdf_hosts_r[0], ccdf_hosts_r[1])
label1 = 'random '+StatLabel(groupSize_r['members'])
plt.legend([p1], [label1], bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of hosts per group')
plt.xscale('log')
plt.ylim(0,1)
plt.grid('on')

plt.subplot(412)
p1, = plt.plot(ccdf_pods_r[0], ccdf_pods_r[1])
label1 = 'random '+StatLabel(groupSize_r['pods'])
plt.legend([p1], [label1], bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of pods per group')
plt.ylim(0,1)
plt.grid('on')

ax3 = plt.subplot(413)
p1, = plt.plot(ccdf_edges_r[0], ccdf_edges_r[1])
label1 = 'random '+StatLabel(groupSize_r['edges'])
plt.legend([p1], [label1], bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of edge switches per pod per group')
plt.ylim(0,1)
plt.grid('on')

ax4 = plt.subplot(414, sharex = ax3)
p1, = plt.plot(ccdf_edges_r[0], ccdf_edges_r[1])
plt.xlabel('number of edge switches per pod per group')
plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')
'''

plt.figure(2)
#plt.suptitle('CCDF of multicast addresses on switches\n dashed -> after aggregation ')
#ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_addr_core_r[0], ccdf_addr_core_r[1], 'b-')
p2, = plt.plot(ccdf_addr_aggr_r[0], ccdf_addr_aggr_r[1], 'g-')
p3, = plt.plot(ccdf_addr_edge_r[0], ccdf_addr_edge_r[1], 'r-')
p4, = plt.plot(ccdf_addr_aggr_aggr[0], ccdf_addr_aggr_aggr[1], 'g--')
label1 = 'core '+StatLabel(coreSwitches_r)
label2 = 'aggr '+StatLabel(aggrSwitches_r)
label3 = 'edge '+StatLabel(edgeSwitches_r)
label4 = 'aggr '+StatLabel(switches_aggr)
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('number of group addresses on a switch')
plt.ylim(0,1)
plt.grid('on')
'''
ax2 = plt.subplot(212, sharex=ax1)
p1, = plt.plot(ccdf_addr_core_r[0], ccdf_addr_core_r[1], 'b-')
p2, = plt.plot(ccdf_addr_aggr_r[0], ccdf_addr_aggr_r[1], 'g-')
p3, = plt.plot(ccdf_addr_edge_r[0], ccdf_addr_edge_r[1], 'r-')
p4, = plt.plot(ccdf_addr_aggr_aggr[0], ccdf_addr_aggr_aggr[1], 'g--')
plt.xlabel('number of group addresses on a switch')
plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')

plt.setp(ax1.get_xticklabels(), visible=False)
'''
plt.figure(3)
#plt.suptitle('CCDF of traffic rate on links\n dashed -> after aggregation')
'''
ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_link_core_r[0], ccdf_link_core_r[1], 'b-')
p2, = plt.plot(ccdf_link_aggr_r[0], ccdf_link_aggr_r[1], 'g-')
p3, = plt.plot(ccdf_link_edge_r[0], ccdf_link_edge_r[1], 'r-')
p4, = plt.plot(ccdf_link_aggr_aggr[0], ccdf_link_aggr_aggr[1], 'g--')
label1 = 'core-aggr '+StatLabel(coreLinks_r)
label2 = 'aggr-edge '+StatLabel(podLinks_r)
label3 = 'edge-host '+StatLabel(edgeLinks_r)
label4 = 'aggr-edge '+StatLabel(links_aggr)
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.ylim(0,1)
plt.grid('on')
'''
#ax2 = plt.subplot(212, sharex=ax1)
p1, = plt.plot(ccdf_link_core_r[0], ccdf_link_core_r[1], 'b-')
p2, = plt.plot(ccdf_link_aggr_r[0], ccdf_link_aggr_r[1], 'g-')
p3, = plt.plot(ccdf_link_edge_r[0], ccdf_link_edge_r[1], 'r-')
p4, = plt.plot(ccdf_link_aggr_aggr[0], ccdf_link_aggr_aggr[1], 'g--')
label1 = 'core-aggr '+StatLabel(coreLinks_r)
label2 = 'aggr-edge '+StatLabel(podLinks_r)
label3 = 'edge-host '+StatLabel(edgeLinks_r)
label4 = 'aggr-edge '+StatLabel(links_aggr)
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,1), loc=4, prop={'size':10}, borderaxespad=0.)
plt.xlabel('traffic rate on a link')
plt.yscale('log')
plt.ylim(0,1)
plt.grid('on')

#plt.setp(ax1.get_xticklabels(), visible=False)

plt.show()
