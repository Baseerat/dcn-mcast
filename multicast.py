#!/usr/bin/python
import random
from network import *
import aggregate as aggr
#random.seed(0)

class AddressDistribution:
    def __init__(self, k, n, r, pa, pb):
        # core switches with l-th block
        self.CoreSet = [0]*n
        # aggregation switches with l-th block in type A pods
        self.AggrSet_A = [0]*n
        # aggregation switches with l-th block in type B pods
        self.AggrSet_B = [0]*n  
        for i in range(n):
            self.CoreSet[i] = set()
            self.AggrSet_A[i] = set()
            self.AggrSet_B[i] = set()

        # block assigned to m-th core switch
        self.Block_C = [0]*pow((k/2),2)
        # blocks assigned to i-th aggregation switch in type A pods  
        self.BlockSet_A = [0]*(k/2) 
        # blocks assigned to i-th aggregation switch in type B pods
        self.BlockSet_B = [0]*(k/2) 
        for i in range(k/2):
            self.BlockSet_A[i] = set()
            self.BlockSet_B[i] = set()

        for l in range(n):
            x = int(k*l/(2*n*pa))
            y = l%(2*n*pa/k)
            for i in range(x*pa, (x+1)*pa):
                for j in range(y*pb, (y+1)*pb):
                    self.CoreSet[l].add(i*k/2+j)

            for i in range(x*pa, (x+1)*pa):
                self.AggrSet_A[l].add(i)
                self.BlockSet_A[i].add(l)

            y = l%(k/(2*pb))
            for i in range(y*pb, (y+1)*pb):
                self.AggrSet_B[l].add(i)
                self.BlockSet_B[i].add(l)
        
        for m in range(pow((k/2),2)):
            self.Block_C[m] = int(int(2*m/k)/pa)*(2*n*pa/k) + int((m%(k/2))/pb)


class Group:
    def __init__(self):
        self.id = -1
        self.block = -1
        self.rate = -1
        self.members = {}
        self.hosts = []
        self.tenant = -1
        self.size = 0

class Groups:
    def __init__(self, k, n, N, tenants, network):
        self.blocks = [0]*n
        for i in range(n):
            self.blocks[i] = set()

        tenantsList = []
        for host in network.hosts['tenants'].keys():
            tenantsList.extend(network.hosts['tenants'][host])
        random.shuffle(tenantsList)

        tenantsG = [0]*len(tenants)

        self.groups = [0]*N
        for i in range(N):
            if i%1000 == 0:
                print 'create group %d'%i
            self.groups[i] = Group()
            self.groups[i].id = i
            self.groups[i].block = i%n
            self.blocks[i%n].add(i)
            self.groups[i].rate = random.randint(1,10)
            #if i < len(tenants):
            #    self.groups[i].tenant = i
            #    sample = tenants[i]
            #else:
            self.groups[i].tenant = random.sample(tenantsList, 1)[0]
            sample = randomSample(tenants[self.groups[i].tenant],'mix3',5)
            tenantsG[self.groups[i].tenant] += 1
            for hostname in sorted(sample):
                IDs = hostname.strip('H').split('.')
                pod_id = int(IDs[0])
                edge_id = int(IDs[1])
                host_id = int(IDs[2])
                if pod_id not in self.groups[i].members.keys():
                    self.groups[i].members[pod_id] = {}
                    network.pods[pod_id].groups.add(i)
                if edge_id not in self.groups[i].members[pod_id].keys():
                    self.groups[i].members[pod_id][edge_id] = set()
                    network.pods[pod_id].edges[edge_id].groups.add(i)
                self.groups[i].members[pod_id][edge_id].add(host_id)
                #network.hosts['groups'][hostname].add(i)
                network.hosts['groups'][hostname] += 1

            self.groups[i].hosts = sample
            self.groups[i].size = len(sample)

        #print tenantsG

    def groupSize(self):
        groupSize = {}
        groupSize['pods'] = [0]*len(self.groups)
        groupSize['edges'] = []
        groupSize['members'] = [0]*len(self.groups)
        for i in range(len(self.groups)):
            groupSize['pods'][i] = len(self.groups[i].members.keys())
            for pod in self.groups[i].members.keys():
                groupSize['edges'].append(len(self.groups[i].members[pod].keys()))
            groupSize['members'][i] = self.groups[i].size
        return groupSize


def Dynamic(group, tenants, network, updates):
    hosts_in = set(group.hosts)
    hosts_out = set(tenants[group.tenant]) - hosts_in
    join = True
    leave = False
    _min = 5

    if len(hosts_out) == 0:
        action = leave
    elif len(hosts_in) == _min:
        action = join
    elif random.random() < 0.504:
        action = join
    else:
        action = leave

    if action == join:
        hostname = random.sample(hosts_out, 1)[0]
    else:
        hostname = random.sample(hosts_in, 1)[0]

    IDs = hostname.strip('H').split('.')
    pod_id = int(IDs[0])
    edge_id = int(IDs[1])
    host_id = int(IDs[2])
    
    if action == join:
        if pod_id not in group.members.keys():
            group.members[pod_id] = {}
            updates['cores_J'] += 9 # needs to be changed!
        if edge_id not in group.members[pod_id].keys():
            group.members[pod_id][edge_id] = set()
            updates['aggrs_J'] += 3 # needs to be changed!
        group.members[pod_id][edge_id].add(host_id)
        updates['edges_J'] += 1

        #network.hosts['groups'][hostname].add(group.id)
        network.hosts['groups'][hostname] += 1
        group.hosts.add(hostname)
        group.size += 1
        
    if action == leave:
        group.members[pod_id][edge_id].remove(host_id)
        updates['edges_L'] += 1
        if len(group.members[pod_id][edge_id]) == 0:
            del group.members[pod_id][edge_id]
            updates['aggrs_L'] += 3 # needs to be changed!
            if(len(group.members[pod_id]) == 0):
                del group.members[pod_id]
                updates['cores_L'] += 9 # needs to be changed!

        #network.hosts['groups'][hostname].remove(group.id)
        network.hosts['groups'][hostname] -= 1
        group.hosts.remove(hostname)
        group.size -= 1
        
    return group


def assignAggrGroups(G, network, distribution):
    for i in range(len(G.groups)):
        group = G.groups[i]
        aggrFlag = 0
        if len(group.members.keys()) > 1:
            aggrFlag = 1
        elif len(group.members.keys()) == 1:
            if len(group.members[group.members.keys()[0]].keys()) > 1:
                aggrFlag = 1
        for pod in group.members.keys():
            if aggrFlag == 1:
                if pod%2 == 0:
                    for i in distribution.AggrSet_A[group.block]:
                        network.pods[pod].aggrs[i].groups.add(group.id)
                else:
                    for i in distribution.AggrSet_B[group.block]:
                        network.pods[pod].aggrs[i].groups.add(group.id)


class multicastTree_simple:
    def __init__(self, group, network, distribution, aggrGroupEdges):
        self.id = group.id
        self.rate = group.rate
        if len(group.members.keys()) > 1:
            self.layer = 3
            for  i in distribution.CoreSet[group.block]:
                network.switches['C%s'%i] += 1
        elif len(group.members.keys()) == 1:
            if len(group.members[group.members.keys()[0]].keys()) > 1:
                self.layer = 2
            else:
                self.layer = 1

        core_id = random.sample(distribution.CoreSet[group.block],1)[0]
        core_name = 'C%s'%core_id
        for pod in group.members.keys():
            if self.layer in [2,3]:
                if pod%2 == 0:
                    for i in distribution.AggrSet_A[group.block]:
                        network.switches['A%s.%s'%(pod,i)] += 1
                        #network.pods[pod].aggrs[i].groups.add(group.id)
                else:
                    for i in distribution.AggrSet_B[group.block]:
                        network.switches['A%s.%s'%(pod,i)] += 1
                        #network.pods[pod].aggrs[i].groups.add(group.id)
            aggr_id = network.cores[core_id].down[pod]
            aggr_name = 'A%s.%s'%(pod,aggr_id)
            link = '%s-%s'%(core_name, aggr_name)
            network.links[link] += self.rate * (self.layer==3)

            for edge in group.members[pod].keys():
                edge_name = 'E%s.%s'%(pod,edge)
                network.switches[edge_name] += 1
                link = '%s-%s'%(aggr_name, edge_name)
                network.links[link] += self.rate * (self.layer in [2,3])

                for host in group.members[pod][edge]:
                    host_name = 'H%s.%s.%s'%(pod,edge,host)
                    link = '%s-%s'%(edge_name, host_name)
                    network.links[link] += self.rate                        

            if len(aggrGroupEdges) > 0:
                for edge in aggrGroupEdges[group.id][pod]:
                    edge_name = 'E%s.%s'%(pod,edge)
                    link = '%s-%s'%(aggr_name, edge_name)
                    network.aggrlinks[link] += self.rate

def GenerateTrees(N, G, network, distribution, aggrGroupEdges):
    Trees = [0]*N
    for i in range(N):
        if i%1000 == 0:
            print 'create tree %d'%i
        Trees[i] = multicastTree_simple(G.groups[i], network, distribution, aggrGroupEdges)
    return Trees


def edgeAggregate(portNum, metaNum, pod_id, edge_id, network, G):
    P = [0]*portNum
    for i in range(portNum):
        P[i] = aggr.Port(i)
    M = [0]*metaNum
    for i in range(metaNum):
        M[i] = aggr.MetaGroup(i)
    groups = network.pods[pod_id].edges[edge_id].groups
    Gr = [0]*len(groups)
    i = 0
    for g_id in groups:
        ports = G.groups[g_id].members[pod_id][edge_id]
        Gr[i] = aggr.Group(i, g_id, ports, G.groups[g_id].rate, P)
        i += 1
    G_unassigned = set(range(len(groups)))
    M_empty = set(range(portNum, metaNum-1))

    while len(G_unassigned) > 0:
        aggr.Aggregate(Gr[G_unassigned.pop()], M, Gr, P, M_empty, portNum)

    linkRate = [0]*2
    linkRate[0] = []
    linkRate[1] = []
    for i in range(portNum):
        linkRate[0].append(P[i].effective)
        linkRate[1].append(P[i].rate)
    switchAddr = [0]*2
    switchAddr[0] = len(groups)
    for i in range(metaNum):
        if len(M[i].ports) > 0:
            switchAddr[1] += 1

    return [linkRate, switchAddr]

def aggregateEdges(k, G, network, C):
    linkRate = [[],[]]
    switchAddr = [[],[]]
    for pod_id in range(k):
        print '-------------------------pod %d'%pod_id
        for edge_id in range(k/2):
            print 'edge %d'%edge_id
            res = edgeAggregate(k/2, C, pod_id, edge_id, network, G)
            linkRate[0].extend(res[0][0])
            linkRate[1].extend(res[0][1])
            switchAddr[0].append(res[1][0])
            switchAddr[1].append(res[1][1])
    aggrFile = open('plot/output/aggregateEdges.py', 'w')
    aggrFile.write('links = '+ str(linkRate)+'\n\n' + 'switches = '+str(switchAddr))
    return [linkRate, switchAddr]


def aggrAggregate(portNum, metaNum, pod_id, aggr_id, network, G, aggrGroupEdges):
    P = [0]*portNum
    for i in range(portNum):
        P[i] = aggr.Port(i)
    M = [0]*metaNum
    for i in range(metaNum):
        M[i] = aggr.MetaGroup(i)

    idmap = {}
    groups = network.pods[pod_id].aggrs[aggr_id].groups
    Gr = [0]*len(groups)
    i = 0
    for g_id in groups:
        ports = set(G.groups[g_id].members[pod_id].keys())
        Gr[i] = aggr.Group(i, g_id, ports, G.groups[g_id].rate, P)
        idmap[g_id] = i
        i += 1
    G_unassigned = set(range(len(groups)))
    M_empty = set(range(portNum, metaNum-1))

    while len(G_unassigned) > 0:
        aggr.Aggregate(Gr[G_unassigned.pop()], M, Gr, P, M_empty, portNum)

    for g_id in groups:
        if g_id not in aggrGroupEdges.keys():
            aggrGroupEdges[g_id] = {}
        aggrGroupEdges[g_id][pod_id] = M[Gr[idmap[g_id]].meta].ports
    
    switchAddr = 0
    for i in range(metaNum):
        if len(M[i].ports)>0:
            switchAddr += 1
    
    return switchAddr

def aggregatePods(k, G, network, pa, pb, C):
    aggrGroupEdges = {}
    for pod_id in range(k):
        print '-------------------------pod %d'%pod_id
        if pod_id%2 == 0:
            for aggr_id in range(0,k/2,pa):
                print 'aggr %d'%aggr_id
                addrNum = aggrAggregate(k/2, C, pod_id, aggr_id, network, G, aggrGroupEdges)
                for i in range(aggr_id, aggr_id+pa):
                    network.aggrs['A%s.%s'%(pod_id, i)] = addrNum
        else:
            for aggr_id in range(0,k/2,pb):
                print 'aggr %d'%aggr_id
                addrNum = aggrAggregate(k/2, C, pod_id, aggr_id, network, G, aggrGroupEdges)
                for i in range(aggr_id, aggr_id+pb):
                    network.aggrs['A%s.%s'%(pod_id, i)] = addrNum

    return aggrGroupEdges
    

def doAggregate(k, G, network, distribution, C, pa, pb, layer):
    aggrGroupEdges = {}
    if layer == 'a': # aggregate on aggreation layer
        assignAggrGroups(G, network, distribution)
        aggrGroupEdges = aggregatePods(k, G, network, pa, pb, C)
    elif layer == 'e': # aggregate on edge layer
        aggregateEdges(k, G, network, C)
    return aggrGroupEdges


def PrintAggregate(args, P, G, M):
    if 'group' in args or 'g' in args:
        for i in range(len(G)):
            aggr.printGroup(G[i])
        print ''
    if 'meta' in args or 'm' in args:
        for i in range(len(M)):
            aggr.printMeta(M[i])
        print ''
    if 'port' in args or 'p' in args:
        for i in range(len(P)):
            aggr.printPort(P[i])
        print ''
    if 'stat' in args or 's' in args:
        totalCost = aggr.TotalCost(P)
        print 'total cost:     ', totalCost[0]
        print 'effective cost: ', totalCost[1]
        effective = 0
        extra = 0
        duplicate = 0
        total = 0
        for i in range(len(M)):
            effective += M[i].metaRate[0]
            duplicate += M[i].metaRate[1]
            extra += M[i].metaRate[2]
        print 'meta rate:      ', [effective, duplicate, extra, extra/float(duplicate)]
'''
        extra_send = []
        extra_recv = []
        for i in range(len(G)):
            extra_send.append(G[i].groupRate[2])
            extra_recv.append(G[i].groupRate[3])
        print 'group extra_send [min, max, mean, median]: ',[min(extra_send), max(extra_send), \
                                                             mean(extra_send), median(extra_send)]
        print 'group extra_recv [min, max, mean, median]: ',[min(extra_recv), max(extra_recv), \
                                                             mean(extra_recv), median(extra_recv)]
'''

def randomSample(population, method, _min):
    N = len(population)
    size = 0
    if method == 'tri': # triangular distribution
        size = int(random.triangular(_min-1, N+3, _min+4))%N+1
    elif method == 'beta': # beta distribution
        size = int((N-_min+1)*random.betavariate(0.6, 0.6))+_min
    elif method == 'norm_r': # reverse norm distribution
        p = random.gauss(0.5,0.25)
        if p < 0.5: p = abs(0.5-p)
        else: p = abs(1.5-p)
        size = int(N*p)%N+1
    elif method == 'expo': # exponential distribution
        size = int(random.expovariate(0.12))%N+1
    elif method == 'expo_r': # reverse exponential distribution
        size = N-int(random.expovariate(0.12))%N
    elif method == 'gamma': # gamma distribution
        size = int(random.gammavariate(2.5,2)*N/15+_min-1)%N+1
    elif method == 'gamma': # gamma distribution
        size = int(random.gammavariate(2.5,2)*N/15+_min-1)%N+1
    elif method == 'mix1':
        seed = random.random()
        if seed < 0.1:
            size = random.randint(_min,N)
        else:
            size = int(random.gammavariate(2.5,0.5)*N/15+_min-1)%N+1
    elif method == 'mix2':
        r = random.random()
        if r < 0.02:
            size = N-int(random.gammavariate(1,0.1)*N/15)%N
        else:
            size = int(random.gammavariate(1.9,0.16)*N/15+_min-1)%N+1
    elif method == 'mix3':
        r = random.random()
        if r < 0.02:
            size = N-int(random.gammavariate(1,0.1)*N/15)%N
        else:
            size = int(random.gammavariate(2,0.2)*N/15+_min-1)%N+1
    elif method == 'mix4':
        r = random.random()
        if r < 0.02:
            size = N-int(random.gammavariate(1,0.1)*N/15)%N
        elif r >= 0.02 and r < 0.52:
            size = random.randint(_min, N)
        else:
            size = int(random.gammavariate(2,0.2)*N/15+_min-1)%N+1
    else: # uniform distribution
        size = random.randint(_min,N)
    size = max(size, _min)
    sample = set(sorted(random.sample(population,size))) 
    return sample

