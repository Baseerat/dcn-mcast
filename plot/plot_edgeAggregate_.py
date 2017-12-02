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
ccdf_addr_core_c = CDF(coreSwitches_c, 1000)
ccdf_addr_aggr_c = CDF(aggrSwitches_c, 1000)
ccdf_addr_edge_c = CDF(edgeSwitches_c, 1000)
ccdf_addr_edge_aggr = CDF(switches[1], 1000)
ccdf_link_core_c = CDF(coreLinks_c, 100)
ccdf_link_aggr_c = CDF(podLinks_c, 1000)
ccdf_link_edge_c = CDF(edgeLinks_c, 10000)
ccdf_link_edge_aggr = CDF(links[1],10000)

plt.figure(1)
#plt.suptitle('CCDF of multicast addresses on switches\n dashed -> after aggregation ')
#plt.subplots_adjust(hspace=1.5)
ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_addr_core_c[0], ccdf_addr_core_c[1], 'b-')
p2, = plt.plot(ccdf_addr_aggr_c[0], ccdf_addr_aggr_c[1], 'g-')
p3, = plt.plot(ccdf_addr_edge_c[0], ccdf_addr_edge_c[1], 'r-')
p4, = plt.plot(ccdf_addr_edge_aggr[0], ccdf_addr_edge_aggr[1], 'r--')
label1 = 'core'
label2 = 'aggr'
label3 = 'edge'
label4 = 'edge'
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,0), loc=4, prop={'size':10})
plt.xlabel('number of multicast addresses on a switch')
#plt.xlim(0,8000)
plt.ylim(0,1)
ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_axisbelow(True)

ax2 = plt.subplot(212)
p1, = plt.plot(ccdf_link_core_c[0], ccdf_link_core_c[1], 'b-')
p2, = plt.plot(ccdf_link_aggr_c[0], ccdf_link_aggr_c[1], 'g-')
p3, = plt.plot(ccdf_link_edge_c[0], ccdf_link_edge_c[1], 'r-')
p4, = plt.plot(ccdf_link_edge_aggr[0], ccdf_link_edge_aggr[1], 'r--')
label1 = 'core-aggr'
label2 = 'aggr-edge'
label3 = 'edge-host'
label4 = 'edge-host'
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,0), loc=4, prop={'size':10})
plt.xlabel('traffic rate on a link')
#plt.xlim(0,30000)
plt.ylim(0,1)
ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax2.set_axisbelow(True)

plt.show()
