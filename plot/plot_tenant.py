#!/usr/bin/python
import matplotlib.pyplot as plt
from utils import *
from output.tenant import *

tenantsLen = []
for i in range(len(tenants)):
    tenantsLen.append(len(tenants[i]))

hostTenants = []
for host in hosts.keys():
    hostTenants.append(len(hosts[host]))

plt.figure(0)
cdf_tenants = CDF(tenantsLen, 1000)
cdf_hosts = CDF(hostTenants, 1000)

plt.figure(1)
plt.subplots_adjust(hspace=0.3)

plt.subplot(211)
#plt.title('CDF of tenant size distribution')
p1, = plt.plot(cdf_tenants[0], cdf_tenants[1])
label1 = StatLabel(tenantsLen)
plt.legend([p1], [label1], bbox_to_anchor=(1,0), loc=4, prop={'size':9})
plt.xlabel('number of hosts per tenant')
#plt.xscale('log')
plt.ylim(0,1)
plt.grid('on')

plt.subplot(212)
#plt.title('CDF of number of tenants per host')
p1, = plt.plot(cdf_hosts[0], cdf_hosts[1])
label1 = StatLabel(hostTenants)
plt.legend([p1], [label1], bbox_to_anchor=(0,1), loc=2, prop={'size':9})
plt.xlabel('number of tenants per host')
plt.ylim(0,1)
#plt.xlim(0,9)
plt.grid('on')

plt.show()
