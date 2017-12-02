#!/usr/bin/python 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Polygon
from utils import *
from output.out import *
from output.aggregateAggrs import *#switches as aggrSwitches, links as aggrLinks

plt.rc('pdf',fonttype = 42)
plt.rc('ps',fonttype = 42)

coreS = []
aggrS = []
edgeS = []
aggrS_ = []

aggrM = []
edgeM = []

coreL = []
aggrL = []
edgeL = []
aggrL_ = []

for switch in switches.keys():
    if switch.find('C') == 0:
        coreS.append(switches[switch])
    if switch.find('A') == 0:
        aggrS.append(switches[switch])
        aggrM.append(switches[switch]-unicast[switch])
    if switch.find('E') == 0:
        edgeS.append(switches[switch])
        edgeM.append(switches[switch]-unicast[switch])

for switch in aggrSwitches.keys():
    aggrS_.append(aggrSwitches[switch])

for link in aggrLinks.keys():
    aggrL_.append(aggrLinks[link])


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

gs = gridspec.GridSpec(2, 1, height_ratios=[5,4])
ax1 = fig.add_subplot(gs[0])
data = [edgeS, aggrS_, aggrS, coreS]
boxplot(edgeM,[1],colors[3],colors[1],ax1)
boxplot(edgeS,[2],colors[0],colors[1],ax1)
boxplot(aggrS_,[3],colors[3],colors[1],ax1)
boxplot(aggrS,[4],colors[0],colors[1],ax1)
boxplot(coreS,[5],colors[0],colors[1],ax1)
plt.tick_params(labelsize=11)
plt.ylim(0.5,5.5)
plt.yticks([1,2,3,4,5], ['(m) E','E','(la) A','A','C'])
plt.xlabel('No. of multicast addresses on a switch',size=11)
ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey')
ax1.set_axisbelow(True)
#plt.figtext(0.6, 0.86, 'after local aggregation  ',
#            backgroundcolor=colors[2], color='blue', weight='roman', size=9)

ax2 = fig.add_subplot(gs[1])
data = [edgeL, aggrL_, aggrL, coreL]
boxplot(edgeL,[1],colors[0],colors[1],ax2)
boxplot(aggrL_,[2],colors[3],colors[1],ax2)
boxplot(aggrL,[3],colors[0],colors[1],ax2)
boxplot(coreL,[4],colors[0],colors[1],ax2)
plt.tick_params(labelsize=11)
plt.ylim(0.5,4.5)
plt.yticks([1,2,3,4], ['E-H','(la) A-E','A-E','C-A'])
plt.xlim(-20, 700)
plt.xlabel('Traffic rate on a link',size=11)
ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey')
ax2.set_axisbelow(True)

plt.show()
