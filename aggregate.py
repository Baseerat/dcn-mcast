import random, math
#random.seed(0)

class Port:
    def __init__(self, ID):
        self.id = ID
        self.subscribe = set()
        self.meta = set()
        self.rate = 0
        self.effective = 0

class Group:
    def __init__(self, ID, name, ports, rate, P):
        self.id = ID
        self.name = name
        self.ports = ports
        self.rate = rate
        self.meta = -1
        #[effective, duplicate, extra_send, extra_recv]
        self.groupRate = [len(ports)*rate, (len(ports)-1)*rate, 0, 0]
        for i in ports:
            P[i].subscribe.add(ID)
            P[i].rate += rate
            P[i].effective += rate
        
class MetaGroup:
    def __init__(self, ID):
        self.id = ID
        self.ports = set()
        self.groups = set()
        self.rate = 0
        self.metaRate = [0,0,0] #[effective, duplicate, extra]
    
# assign group G to meta-group M. P is all ports.
def Assign(group, meta, P, G):
    if group.id in meta.groups:
        error = 'group [%d] is already in meta-group [%d]'%(group.id, meta.id)
        sys.exit(error)

    for i in meta.ports - group.ports:
        P[i].rate += group.rate
    for i in group.ports - meta.ports:
        P[i].rate += meta.rate
        P[i].meta.add(meta.id)

    group.groupRate[2] = len(meta.ports-group.ports)*group.rate
    for i in meta.groups:
        G[i].groupRate[2] += len(group.ports - meta.ports)*G[i].rate
        G[i].groupRate[3] += len(G[i].ports - group.ports)*group.rate
        group.groupRate[3] += len(group.ports - G[i].ports)*G[i].rate

    group.meta = meta.id
    meta.groups.add(group.id)
    meta.ports.update(group.ports)
    meta.rate += group.rate

    meta.metaRate[0] += group.groupRate[0]
    meta.metaRate[1] += group.groupRate[1]
    meta.metaRate[2] = len(meta.ports)*meta.rate - meta.metaRate[0]

    #meta.metaRate = metaRate(meta, G)

# remove group G from meta-group M. G is all groups, P is all ports.
def Remove(group, meta, P, G, M_empty):
    if group.id not in meta.groups:
        error = 'group [%d] is not in meta-group [%d]'%(group.id, meta.id)
        sys.exit(error)

    leaving = group.ports.copy()
    for i in meta.groups:
        if i != group.id:
            leaving -= G[i].ports
    meta.ports -= leaving
    meta.rate -= group.rate
    meta.groups.remove(group.id)
    if len(meta.groups) == 0:
        M_empty.add(meta.id)

    for i in meta.ports - group.ports:
        P[i].rate -= group.rate
    for i in leaving:
        P[i].rate -= meta.rate
        P[i].meta.remove(meta.id)

    group.groupRate[2] = 0
    group.groupRate[3] = 0
    for i in meta.groups:
        G[i].groupRate[2] -= len(group.ports - meta.ports)*G[i].rate
        G[i].groupRate[3] -= len(G[i].ports - group.ports)*group.rate

    meta.metaRate[0] -= group.groupRate[0]
    meta.metaRate[1] -= group.groupRate[1]
    meta.metaRate[2] = len(meta.ports)*meta.rate - meta.metaRate[0]


def removeGain(group, meta, G):
    leaving = group.ports.copy()
    for i in meta.groups:
        if i != group.id:
            leaving -= G[i].ports    
            
    reduceRate = len(meta.ports)*meta.rate - group.groupRate[0]   \
                 - len(meta.ports-leaving)*(meta.rate-group.rate)

    return reduceRate

def reAggregate(meta, G, P, M, M_empty):
    reduced = 0
    leaving = -1
    for i in meta.groups:
        res = removeGain(G[i], meta, G)
        if reduced <= res:
            reduced = res
            leaving = i
    if reduced >= meta.metaRate[0]*0.1:
        Remove(G[leaving], meta, P, G, M_empty)
        Aggregate(G[leaving], M, G, P, M_empty, len(P))

def groupRate(group, meta, G):
    effective = len(group.ports)*group.rate
    duplicate = (len(group.ports)-1)*group.rate
    extra_send = len(meta.ports-group.ports)*group.rate
    extra_recv = 0
    for i in meta.groups:
        extra_recv += len(group.ports-G[i].ports)*G[i].rate
    return [effective, duplicate, extra_send, extra_recv]

def metaRate(meta, G):
    effective = 0
    duplicate = 0
    for i in meta.groups:
        G[i].groupRate = groupRate(G[i], meta, G)
        effective += G[i].groupRate[0]
        duplicate += G[i].groupRate[1]
    extra = len(meta.ports)*meta.rate - effective
    return [effective, duplicate, extra]

def Diff(group, meta, G):
    extraRate = len(meta.ports-group.ports)*group.rate + len(group.ports-meta.ports)*meta.rate
    if extraRate < min(len(group.ports)*group.rate, meta.metaRate[0])/5:
        diff = False
    else:
        diff = True
    return diff

def Aggregate(group, M, G, P, M_empty, th_B):
    if len(group.ports) >= th_B:
        Assign(group, M[len(M)-1], P, G) #to the broadcast channel
    elif len(group.ports) == 1:
        Assign(group, M[list(group.ports)[0]], P, G) # to related unicast channel
    else:
        cost = 9e+100
        index = -1
        for i in set(range(1, len(M))) - M_empty:
            aggrCost = AggregateCost(group, M[i], P)
            if cost > aggrCost:
                cost = aggrCost
                index = i
        if len(M_empty) > 0 and Diff(group, M[index], G):
            Assign(group, M[M_empty.pop()], P, G)
        else:
            Assign(group, M[index], P, G)

# extra cost when a group is assigned to a meta-group
def AggregateCost(group, meta, P):
    #extraCost = 0
    #for i in meta.ports - group.ports:
    #    extraCost += linkCost(P[i].rate + group.rate) - linkCost(P[i].rate)
    #for i in group.ports - meta.ports:
    #    extraCost += linkCost(P[i].rate + meta.rate) - linkCost(P[i].rate)
    extraCost = len(meta.ports-group.ports)*group.rate + len(group.ports-meta.ports)*meta.rate
    
    return extraCost

# a set of ports join a group
def Join(ports, group, meta, P, G):
    if len(ports & group.ports) > 0:
        error = 'group [%d] already has joining ports'%(group.id)
        sys.exit(error)
    for port_id in ports:
        P[port_id].subscribe.add(group.id)
        P[port_id].effective += group.rate
        if port_id not in meta.ports:
            P[port_id].meta.add(group.meta)
            P[port_id].rate += meta.rate

    group.groupRate[0] += len(ports)*group.rate
    group.groupRate[1] += len(ports)*group.rate
    group.groupRate[2] -= len(ports & meta.ports)*group.rate
    for i in (meta.groups - set([group.id])):
        G[i].groupRate[2] += len(ports-meta.ports)*G[i].rate
        G[i].groupRate[3] -= len(ports & G[i].ports)*group.rate
        group.groupRate[3] += len(ports-G[i].ports)*G[i].rate

    group.ports.update(ports)

    meta.ports.update(ports)
    meta.metaRate[0] += len(ports)*group.rate
    meta.metaRate[1] += len(ports)*group.rate
    meta.metaRate[2] = len(meta.ports)*meta.rate - meta.metaRate[0]

# a set of ports leave a group
def Leave(ports, group, meta, P, G):
    if (ports <= group.ports) == False:
        error = 'group [%d] does not have leaving ports'%(group.id)
        sys.exit(error)
    for port_id in ports:
        P[port_id].subscribe.discard(group.id)
        P[port_id].effective -= group.rate
    group.ports -= ports

    leaving = ports.copy()
    for group_id in meta.groups:
        if group_id != group.id:
            leaving -= G[group_id].ports
    for port_id in leaving:
        P[port_id].meta.remove(group.meta)
        P[port_id].rate -= meta.rate
    meta.ports -= leaving

    group.groupRate[0] -= len(ports)*group.rate
    group.groupRate[1] -= len(ports)*group.rate
    group.groupRate[2] += len(ports & meta.ports)*group.rate
    for i in (meta.groups - set([group.id])):
        G[i].groupRate[2] -= len(ports-meta.ports)*G[i].rate
        G[i].groupRate[3] += len(ports & G[i].ports)*group.rate
        group.groupRate[3] -= len(ports-G[i].ports)*G[i].rate

    meta.metaRate[0] -= len(ports)*group.rate
    meta.metaRate[1] -= len(ports)*group.rate
    meta.metaRate[2] = len(meta.ports)*meta.rate - meta.metaRate[0]

# total link cost for all ports
def TotalCost(P):
    total = 0
    effective = 0
    for i in range(len(P)):
        total += linkCost(P[i].rate)
        effective += linkCost(P[i].effective)
    return [total, effective]

def linkCost(r):
    cost = r
    #cost = r/float(10)+math.pow(2,r/float(1500))
    return cost

def randomSample(ports, distribution):
    N = len(ports)
    size = 0
    if distribution == 'uniform':
        size = random.randint(1,N)
    elif distribution == 'triangular':
        size = int(random.triangular(0, N+3, 4))%N+1
    elif distribution == 'beta':
        size = int(N*random.betavariate(0.6, 0.6))+1
    elif distribution == 'norm_r':
        p = random.gauss(0.5,0.25)
        if p < 0.5: p = abs(0.5-p)
        else: p = abs(1.5-p)
        size = int(N*p)%N+1
    elif distribution == 'expo':
        size = int(random.expovariate(0.12))%N+1
    elif distribution == 'expo_r':
        size = N-int(random.expovariate(0.12))%N
    sample = set(sorted(random.sample(ports,size)))
    return sample

def mean(array):
    return sum(array)/float(len(array))

def median(array):
    values = sorted(array)
    if len(values) % 2 == 1:
        return values[(len(values)+1)/2-1]
    else:
        lower = values[len(values)/2-1]
        upper = values[len(values)/2]
        return (float(lower + upper)) / 2


def printPort(port):
    print '--------------------------------------------'
    print 'port:       ', port.id
    print 'groups:     ', sorted(list(port.subscribe))
    print 'meta-groups:', sorted(list(port.meta))
    print 'rate:       ', port.rate
    print 'effective:  ', port.effective

def printGroup(group):
    print '============================================'
    print 'group:      ', group.id
    print 'ports:      ', sorted(list(group.ports))
    print 'rate:       ', group.rate
    print 'meta-group: ', group.meta
    print 'groupRate:  ', group.groupRate

def printMeta(meta):
    print '++++++++++++++++++++++++++++++++++++++++++++'
    print 'meta-group: ', meta.id
    print 'ports:      ', sorted(list(meta.ports))
    print 'groups:     ', sorted(list(meta.groups))
    print 'rate:       ', meta.rate
    print 'metaRate:   ', meta.metaRate
