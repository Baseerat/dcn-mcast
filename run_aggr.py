#!/usr/bin/python
import random
from aggregate import *
import matplotlib.pyplot as plt

portNum  = 24
groupNum = 3000
metaNum  = 1000

def initialize(portNum, groupNum, metaNum):
    P = [0]*portNum
    G = [0]*groupNum
    M = [0]*metaNum
    G_unassigned = set(range(groupNum)) # groups which are not assigned to meta-groups
    M_empty = set(range(portNum, metaNum-1)) # meta-groups which have no group

    for i in range(portNum):
        P[i] = Port(i)

    for i in range(groupNum):
        ports = randomSample(range(portNum), 'expo')
        rate = random.randint(1, 10)
        G[i] = Group(i, i, ports, rate, P)

    for i in range(metaNum):
        M[i] = MetaGroup(i)

    return [P, G, M, G_unassigned, M_empty]

def simpleAggregation(P, G, M, G_unassigned, M_empty, th_B):
    count = 0
    while len(G_unassigned) > 0:        
        Aggregate(G[G_unassigned.pop()], M, G, P, M_empty, th_B)
        count += 1
        if count %1000 == 0:
            print 'aggregated %d groups'%count

def deAggregateAll(P, G, M, G_unassigned, M_empty):
    for i in range(len(G)):
        if i not in G_unassigned:
            Remove(G[i], M[G[i].meta], P, G, M_empty)
            G_unassigned.add(i)
        if (i+1) %1000 == 0:
            print 'de-aggregated %d groups'%(i+1)

def reAggregateAll(P, G, M, G_unassigned, M_empty):
    for i in range(len(M)):
        if i not in M_empty:
            reAggregate(M[i], G, P, M, M_empty)

def groupDynamic(group, P, G, M, M_empty):
    ports_in = group.ports
    ports_out = set(range(len(P))) - group.ports
    join = True
    leave = False
    if (random.random() < 0.5 and len(ports_out) != 0) or len(ports_in) == 1:
        action = join
        ports = set(random.sample(ports_out, 1))
    else:
        action = leave
        ports = set(random.sample(ports_in, 1))

    if action == join:
        Join(ports, group, M[group.meta], P, G)
    if action == leave:
        Leave(ports, group, M[group.meta], P, G)

    #reAggregate(M[group.meta], G, P, M, M_empty)
    


def main():
    init = initialize(portNum, groupNum, metaNum)
    P = init[0]
    G = init[1]
    M = init[2]
    G_unassigned = init[3]
    M_empty = init[4]

    simpleAggregation(P, G, M, G_unassigned, M_empty, portNum)
    Print(['s'], P, G, M)
'''
    for i in range(groupNum):
        groupDynamic(G[i], P, G, M, M_empty)
        if (i+1) %100 == 0:
            print 'dynamic %d groups'%(i+1)
    Print(['s'], P, G, M)    
        
    for i in range(10):
        reAggregateAll(P, G, M, G_unassigned, M_empty)
        Print(['s'], P, G, M)
'''
    
def Print(args, P, G, M):
    
    if 'group' in args or 'g' in args:
        for i in range(groupNum):
            printGroup(G[i])
        print ''
    if 'meta' in args or 'm' in args:
        for i in range(metaNum):
            printMeta(M[i])
        print ''
    if 'port' in args or 'p' in args:
        for i in range(portNum):
            printPort(P[i])    
        print ''
    if 'stat' in args or 's' in args:
        totalCost = TotalCost(P)
        print 'total cost:     ', totalCost[0]
        print 'effective cost: ', totalCost[1]
        effective = 0
        extra = 0
        duplicate = 0
        for i in range(len(M)):
            effective += M[i].metaRate[0]
            duplicate += M[i].metaRate[1]
            extra += M[i].metaRate[2]
        if duplicate == 0:
            print 'meta rate:      [%d, %d, %d]'%(effective, duplicate, extra)
        else:
            print 'meta rate:      [%d, %d, %d, %.2f]'%(effective, duplicate, extra, extra/float(duplicate))
        extra_send = []
        extra_recv = []
        group_rate = []
        for i in range(len(G)):
            group_rate.append(G[i].groupRate[0])
            extra_send.append(G[i].groupRate[2])
            extra_recv.append(G[i].groupRate[3])
        print 'group total rate [min, max, mean, median]: [%d, %d, %.2f, %.1f]'\
            %(min(group_rate), max(group_rate), mean(group_rate), median(group_rate))
        print 'group extra_send [min, max, mean, median]: [%d, %d, %.2f, %.1f]'\
            %(min(extra_send), max(extra_send), mean(extra_send), median(extra_send))
        print 'group extra_recv [min, max, mean, median]: [%d, %d, %.2f, %.1f]'\
            %(min(extra_recv), max(extra_recv), mean(extra_recv), median(extra_recv))

def Plot(P, G, M):
    linkEffective = []
    linkRate = []

if __name__ == "__main__":
    main()
