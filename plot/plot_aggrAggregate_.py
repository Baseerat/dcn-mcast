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
ccdf_addr_core_r = CDF(coreSwitches_r, 1000)
ccdf_addr_aggr_r = CDF(aggrSwitches_r, 1000)
ccdf_addr_edge_r = CDF(edgeSwitches_r, 1000)
ccdf_link_core_r = CDF(coreLinks_r, 100)
ccdf_link_aggr_r = CDF(podLinks_r, 1000)
ccdf_link_edge_r = CDF(edgeLinks_r, 1000)
ccdf_addr_aggr_aggr = CDF(switches_aggr, 1000)
ccdf_link_aggr_aggr = CDF(links_aggr,1000)

plt.figure(2)
#plt.suptitle('CCDF of multicast addresses on switches\n dashed -> after aggregation ')
#plt.subplots_adjust(hspace=1.5)
ax1 = plt.subplot(211)
p1, = plt.plot(ccdf_addr_core_r[0], ccdf_addr_core_r[1], 'b-')
p2, = plt.plot(ccdf_addr_aggr_r[0], ccdf_addr_aggr_r[1], 'g-')
p3, = plt.plot(ccdf_addr_edge_r[0], ccdf_addr_edge_r[1], 'r-')
p4, = plt.plot(ccdf_addr_aggr_aggr[0], ccdf_addr_aggr_aggr[1], 'g--')
label1 = 'core'
label2 = 'aggr'
label3 = 'edge'
label4 = 'aggr'
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,0), loc=4, prop={'size':10})
plt.xlabel('number of multicast addresses on a switch')
plt.xlim(0,2000)
plt.ylim(0,1)
ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_axisbelow(True)

ax2 = plt.subplot(212)
p1, = plt.plot(ccdf_link_core_r[0], ccdf_link_core_r[1], 'b-')
p2, = plt.plot(ccdf_link_aggr_r[0], ccdf_link_aggr_r[1], 'g-')
p3, = plt.plot(ccdf_link_edge_r[0], ccdf_link_edge_r[1], 'r-')
p4, = plt.plot(ccdf_link_aggr_aggr[0], ccdf_link_aggr_aggr[1], 'g--')
label1 = 'core-aggr'
label2 = 'aggr-edge'
label3 = 'edge-host'
label4 = 'aggr-edge'
plt.legend([p1,p2,p3,p4], [label1, label2, label3, label4], \
               bbox_to_anchor=(1,0), loc=4, prop={'size':10})
plt.xlabel('traffic rate on a link')
plt.ylim(0,1)
ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax2.set_axisbelow(True)

plt.show()
