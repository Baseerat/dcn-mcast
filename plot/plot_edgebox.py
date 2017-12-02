#!/usr/bin/python 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from utils import *
from output.out import *
from output.aggregateEdges import switches as edgeSwitches, links as edgeLinks

plt.rc('pdf',fonttype = 42)
plt.rc('ps',fonttype = 42)

coreS = []
aggrS = []
edgeS = []
edgeS_ = edgeSwitches[1]
aggrM = []
edgeM = []

coreL = []
aggrL = []
edgeL = []
edgeL_ = edgeLinks[1]

for switch in switches.keys():
    if switch.find('C') == 0:
        coreS.append(switches[switch])
    if switch.find('A') == 0:
        aggrS.append(switches[switch])
        aggrM.append(switches[switch]-unicast[switch])
    if switch.find('E') == 0:
        edgeS.append(switches[switch])
        edgeM.append(switches[switch]-unicast[switch])

print max(aggrS)

for link in links.keys():
    if link.find('C') == 0:
        coreL.append(links[link])
    elif link.find('A') == 0:
        aggrL.append(links[link])
    elif link.find('E') == 0:
        edgeL.append(links[link])

def boxplot(data,pos,linecolor,boxcolor,ax):
    bp = plt.boxplot(data,vert=0,whis=5,positions=pos,widths=0.5)
    plt.setp(bp['boxes'], color=linecolor)
    plt.setp(bp['whiskers'], color=linecolor, linestyle='-')
    plt.setp(bp['medians'], color=linecolor)
    plt.setp(bp['fliers'], color=linecolor, marker='+')
    plt.setp(bp['caps'], color=linecolor)

    box = bp['boxes'][0]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = zip(boxX,boxY)
    boxPolygon = Polygon(boxCoords, facecolor=boxcolor)
    ax.add_patch(boxPolygon)

    med = bp['medians'][0]
    plt.plot([np.average(data)], [np.average(med.get_ydata())],
             color='w', marker='.', markeredgecolor=linecolor)

    return bp

fig = plt.figure()
colors = ['black','white','grey','blue','forestgreen','orangered','darkviolet','crimson']

ax1 = fig.add_subplot(211)
boxplot(edgeS_,[1],colors[3],colors[1],ax1)
boxplot(edgeS,[2],colors[0],colors[1],ax1)
#boxplot(aggrM,[3],colors[0],colors[1],ax1)
boxplot(aggrS,[3],colors[0],colors[1],ax1)
boxplot(coreS,[4],colors[0],colors[1],ax1)
plt.ylim(0.5,4.5)
plt.tick_params(labelsize=11)
plt.yticks([1,2,3,4], ['(la) E','E','A','C'],size=11)
plt.xlabel('No. of multicast addresses on a switch',size=11)
ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey')
ax1.set_axisbelow(True)
#plt.figtext(0.6, 0.86, 'after local aggregation  ',
#            backgroundcolor=colors[2], color='blue', weight='roman', size=9)

ax2 = fig.add_subplot(212)
boxplot(edgeL_,[1],colors[3],colors[1],ax2)
boxplot(edgeL,[2],colors[0],colors[1],ax2)
boxplot(aggrL,[3],colors[0],colors[1],ax2)
boxplot(coreL,[4],colors[0],colors[1],ax2)
plt.ylim(0.5,4.5)
plt.xlim(-1000, 26000)
plt.tick_params(labelsize=11)
plt.yticks([1,2,3,4], ['(la) E-H','E-H','A-E','C-A'],size=11)
plt.xlabel('Traffic rate on a link',size=11)
ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey')
ax2.set_axisbelow(True)

plt.show()
