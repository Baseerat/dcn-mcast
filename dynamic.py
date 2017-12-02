#!/usr/bin/python
import math
import random

mFile = open('dynamic_plot.m', 'w')

def mean(array):
    return round(sum(array)/float(len(array)),3)

def median(array):
    values = sorted(array)
    if len(values) % 2 == 1:
        return values[(len(values)+1)/2-1]
    else:
        lower = values[len(values)/2-1]
        upper = values[len(values)/2]
        return float((lower + upper)) / 2

Hosts = set()
for pod in range(8):
    for edge in range(24):
        for host in range(24):
            hostname = '%d.%d.%d'%(pod,edge,host)
            Hosts.add(hostname)

def computeDistribution(N_hosts, rounds):
    podsN = []
    edgesN = []
    podsN_ = []
    edgesN_ = []
    for i in range(rounds):
        if i%500 == 0:
            print i
        Pods = {}
        Edges = {}
        sample = random.sample(Hosts, N_hosts)
        for hostname in sample:
            ids = hostname.split('.')
            pod = int(ids[0])
            edge = int(ids[1])
            host = int(ids[2])
            edgename = '%d.%d'%(pod, edge)
            if pod not in Pods.keys():
                Pods[pod]=0
            Pods[pod] += 1
            if edgename not in Edges.keys():
                Edges[edgename] = 0
            Edges[edgename] += 1
        podsN.append(len(Pods.keys()))
        edgesN.append(len(Edges.keys()))
        podn = 0
        for pod in Pods.keys():
            if Pods[pod] == 1:
                podn += 1
        podsN_.append(podn)
        edgen = 0
        for edge in Edges.keys():
            if Edges[edge] == 1:
                edgen += 1
        edgesN_.append(edgen)

    return [mean(podsN), mean(edgesN), mean(podsN_), mean(edgesN_)]

def computeUpdates(N, distribution):
    p_join = 1/float(4608-N)
    N_join = 1 + 3*(192-distribution[1])*24*p_join \
             + 9*(8-distribution[0])*576*p_join

    p_leave = 1/float(N)
    N_leave = 1 + 3*distribution[3]*p_leave + 9*distribution[2]*p_leave

    N_burst = float(N + 3*distribution[1] + 9*distribution[0])/N
    N_batch = float(distribution[1] + 3*distribution[0] + 9)/N

    return [round(N_join,3), round(N_leave,3), round(N_burst,3), round(N_batch,3)]

sample = [10,20,30,40,60,80,100,120,150,200,250,300, \
          350,400,500,600,700,800,900,1000]


distribution = []
updates = []

for N in sample:
    print 'Number of hosts = %d'%N
    dist = computeDistribution(N, 5000)
    distribution.append(dist)
    updates.append(computeUpdates(N, dist))


N_join = []
N_leave = []
N_burst = []
N_batch = []
for i in range(len(sample)):
    print distribution[i]
    N_join.append(updates[i][0])
    N_leave.append(updates[i][1])
    N_burst.append(updates[i][2])
    N_batch.append(updates[i][3])

print N_join
print N_leave
print N_burst
print N_batch

mFile.write('size = '+str(sample)+';\n\n' \
            +'N_join = '+str(N_join)+';\n\n' \
            +'N_leave = '+str(N_leave)+';\n\n' \
            +'N_burst = '+str(N_burst)+';\n\n' \
            +'N_batch = '+str(N_batch)+';\n\n')
