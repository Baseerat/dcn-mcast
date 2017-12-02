#!/usr/bin/python
import random
random.seed(0)

class Switch:
    def __init__(self, k, layer, ID):
        self.k = k
        self.layer = layer
        self.groups = set()
        if layer == 1:  # edge switch
            self.up = range(k/2)
            self.down = range(k/2)
            self.name = 'E%d.%d'%(ID[0],ID[1])
        elif layer == 2: # aggregation switch
            self.up = [-1]*(k/2)
            self.down = range(k/2)
            self.name = 'A%d.%d'%(ID[0],ID[1])
        elif layer == 3: # core switch
            self.up = -1
            self.down = [-1]*k
            self.name = 'C%d'%ID
        else:
            self.up = -1
            self.down = -1


class Pod:
    def __init__(self, k, pod_id):
        self.k = k
        self.id = pod_id        
        self.type = ''
        self.groups = set()

        self.edges = [0]*(k/2)
        for i in range(k/2):
            self.edges[i] = Switch(k, 1, [pod_id, i])

        self.aggrs = [0]*(k/2)
        for i in range(k/2):
            self.aggrs[i] = Switch(k, 2, [pod_id, i])

class ABFatTree:
    def __init__(self, k):
        self.k = k
        self.links = {}
        self.switches = {}
        self.hosts = {}
        self.hosts['tenants'] = {}
        self.hosts['groups'] = {}

        self.aggrs = {}
        self.aggrlinks = {}

        self.cores = [0]*pow((k/2),2)
        for i in range(pow((k/2),2)):
            self.cores[i] = Switch(k, 3, i)
            self.switches[self.cores[i].name] = 0

        self.pods = [0]*k
        for i in range(k):
            #print 'create pod %d'%i
            self.pods[i] = Pod(k, i)
            if i%2 == 0:
                self.pods[i].type = 'A'
                for j in range(k/2):
                    for h in range(k/2):
                        self.pods[i].aggrs[j].up[h] = j*k/2+h
                        self.cores[j*k/2+h].down[i] = j
                        link = '%s-A%s.%s'%(self.cores[j*k/2+h].name,i,j)
                        self.links[link] = 0
            elif i%2 == 1:
                self.pods[i].type = 'B'
                for j in range(k/2):
                    for h in range(k/2):
                        self.pods[i].aggrs[j].up[h] = j+h*k/2
                        self.cores[j+h*k/2].down[i] = j
                        link = '%s-A%s.%s'%(self.cores[j+h*k/2].name,i,j)
                        self.links[link]= 0

        for p in range(k):
            for a in range(k/2):
                self.switches[self.pods[p].aggrs[a].name] = 0
                self.aggrs[self.pods[p].aggrs[a].name] = 0 # for aggr switches aggregation
                for e in range(k/2):
                    link = 'A%d.%d-E%d.%d'%(p,a, p,e)
                    self.links[link] = 0
                    self.aggrlinks[link] = 0 # for aggr switches aggregation
            for e in range(k/2):
                self.switches[self.pods[p].edges[e].name] = 0
                for h in range(k/2):
                    link = 'E%d.%d-H%d.%d.%d'%(p,e, p,e,h)
                    self.links[link] = 0
                    host = 'H%d.%d.%d'%(p,e,h)
                    self.hosts['tenants'][host] = set()
                    #self.hosts['groups'][host] = set()
                    self.hosts['groups'][host] = 0

def Tenants(network, TN, _min, _max, mode):
    C = 8
    tenants = []
    hosts_avaliable = set(network.hosts['tenants'].keys())
    hosts_in_pods = Hosts_in_Pods(hosts_avaliable)
    for i in range(TN):
        r = random.random()
        if r < 0.02:
            size = random.randint(_min, _max)
        else:
            size = int((random.expovariate(2)/10)*(_max-_min))%(_max-_min)+_min
        tenant = []
        if mode in ['random', 'r']:
            tenant = random.sample(hosts_avaliable, size)
            for host in tenant:
                network.hosts['tenants'][host].add(i)
                if len(network.hosts['tenants'][host]) >= C:
                    hosts_avaliable.remove(host)
        elif mode in ['collocate', 'c']:
            usedPods = set()
            while len(tenant) < size:
                pod_id = random.sample(set(hosts_in_pods.keys())-usedPods, 1)[0]
                usedPods.add(pod_id)
                if size-len(tenant) < len(hosts_in_pods[pod_id]):
                    tenant.extend(Sample_in_Pod(hosts_in_pods[pod_id], size-len(tenant)))
                else:
                    tenant.extend(list(hosts_in_pods[pod_id]))
            for host in tenant:
                network.hosts['tenants'][host].add(i)
                if len(network.hosts['tenants'][host]) >= C:
                    pod_id = int(host.strip('H').split('.')[0])
                    hosts_in_pods[pod_id].remove(host)
                    if len(hosts_in_pods[pod_id]) == 0:
                        del hosts_in_pods[pod_id]     
        tenants.append(sorted(tenant))
 
    return tenants


def Tenants_(network, TN, _min, _max, mode):
    C = 20
    tenants = []
    tenantSize = []
    hosts_avaliable = set(network.hosts['tenants'].keys())
    hosts_in_pods = Hosts_in_Pods(hosts_avaliable)
    space_in_pods = Space_in_Pods(hosts_in_pods)
    #print space_in_pods

    for i in range(TN):
        r = random.random()
        if r < 0.02:
            size = random.randint(_min, _max)
        else:
            size = int((random.expovariate(4)/10)*(_max-_min))%(_max-_min)+_min
        #print size
        tenantSize.append(size)
    
    #tenantSize = sorted(tenantSize)
    for i in range(TN):
        size = tenantSize.pop()
        #print size
        tenant = []
        if mode in ['random', 'r']:
            tenant = random.sample(hosts_avaliable, size)
            for host in tenant:
                network.hosts['tenants'][host].add(i)
                if len(network.hosts['tenants'][host]) >= C:
                    hosts_avaliable.remove(host)
        elif mode in ['collocate', 'c']:
            sorted_pods = sorted(space_in_pods.items(), key=lambda x: x[1])
            #print sorted_pods
            #usedPods = set()
            while len(tenant) < size:
                pod_id = sorted_pods.pop()[0]
                #pod_id = random.sample(set(hosts_in_pods.keys())-usedPods, 1)[0]
                #usedPods.add(pod_id)
                if size-len(tenant) < len(hosts_in_pods[pod_id]):
                    tenant.extend(Sample_in_Pod(hosts_in_pods[pod_id], size-len(tenant)))
                else:
                    tenant.extend(list(hosts_in_pods[pod_id]))
            for host in tenant:
                network.hosts['tenants'][host].add(i)
                if len(network.hosts['tenants'][host]) >= C:
                    pod_id = int(host.strip('H').split('.')[0])
                    hosts_in_pods[pod_id].remove(host)
                    space_in_pods[pod_id] -= 1
                    if len(hosts_in_pods[pod_id]) == 0:
                        del hosts_in_pods[pod_id]
                        del space_in_pods[pod_id]
        tenants.append(sorted(tenant))
    print space_in_pods

    return tenants

def Sample_in_Pod(hosts_in_pod, size):
    hosts = []
    usedEdges = set()
    hosts_in_edges = Hosts_in_Edges(hosts_in_pod)
    while len(hosts) < size:
        edge_id = random.sample(set(hosts_in_edges.keys())-usedEdges, 1)[0]
        usedEdges.add(edge_id)
        if size-len(hosts) < len(hosts_in_edges[edge_id]):
            hosts.extend(random.sample(hosts_in_edges[edge_id], size-len(hosts)))
        else:
            hosts.extend(list(hosts_in_edges[edge_id]))
    return hosts

def Hosts_in_Pods(hosts):
    hosts_in_pods = {}
    for host in hosts:
        pod_id = int(host.strip('H').split('.')[0])
        if pod_id not in hosts_in_pods.keys():
            hosts_in_pods[pod_id] = set()
        hosts_in_pods[pod_id].add(host)
    return hosts_in_pods

def Space_in_Pods(hosts_in_pods):
    space_in_pods = {}
    for pod_id in hosts_in_pods.keys():
        space_in_pods[pod_id] = len(hosts_in_pods[pod_id])
    return space_in_pods

def Hosts_in_Edges(hosts_in_pod):
    hosts_in_edges = {}
    for host in hosts_in_pod:
        edge_id = int(host.strip('H').split('.')[1])
        if edge_id not in hosts_in_edges.keys():
            hosts_in_edges[edge_id] = set()
        hosts_in_edges[edge_id].add(host)
    return hosts_in_edges

def Tenants_x(network, _min, _max, mode):
    tenants = []
    hosts_avaliable = set(network.hosts['tenants'].keys())
    hosts_in_pods = Hosts_in_Pods(hosts_avaliable)
    i = 0
    while len(hosts_avaliable) > _max:
        size = int((random.expovariate(2)/5)*(_max-_min))%(_max-_min)+_min
        tenant = []
        if mode in ['collocate', 'c']:
            usedPods = set()
            while len(tenant) < size:
                pod_id = random.sample(set(hosts_in_pods.keys())-usedPods, 1)[0]
                usedPods.add(pod_id)
                if size-len(tenant) < len(hosts_in_pods[pod_id]):
                    tenant.extend(Sample_in_Pod(hosts_in_pods[pod_id], size-len(tenant)))
                else:
                    tenant.extend(list(hosts_in_pods[pod_id]))
            for host in tenant:
                network.hosts['tenants'][host].add(i)
                pod_id = int(host.strip('H').split('.')[0])
                hosts_in_pods[pod_id].remove(host)
                if len(hosts_in_pods[pod_id]) == 0:
                    del hosts_in_pods[pod_id]
        elif mode in ['random', 'r']:
            tenant = sorted(random.sample(hosts_avaliable,size))
            for host in tenant:
                network.hosts['tenants'][host].add(i)

        hosts_avaliable -= set(tenant)        
        tenants.append(sorted(tenant))
        i += 1

    for host in hosts_avaliable:
        network.hosts['tenants'][host].add(i)
    tenants.append(sorted(list(hosts_avaliable)))

    return tenants
