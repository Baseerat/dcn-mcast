#!/usr/bin/python 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from utils import *
from output.out import *

coreS = []
aggrS = []
edgeS = []

aggrM = []
edgeM = []

for switch in switches.keys():
    if switch.find('C') == 0:
        coreS.append(switches[switch])
    if switch.find('A') == 0:
        aggrS.append(switches[switch])
        aggrM.append(switches[switch]-unicast[switch])
    if switch.find('E') == 0:
        edgeS.append(switches[switch])
        edgeM.append(switches[switch]-unicast[switch])

data = [coreS, aggrS, edgeS]

fig = plt.figure()
fig.canvas.set_window_title('A Boxplot Example')
ax1 = fig.add_subplot(111)
#plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=5)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='+')

ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_axisbelow(True)

boxColors = ['green','darkkhaki','royalblue']
numBoxes = 3
medians = range(numBoxes)
for i in range(numBoxes):
    box = bp['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = zip(boxX,boxY)
    boxPolygon = Polygon(boxCoords, facecolor=boxColors[i])
    ax1.add_patch(boxPolygon)

    med = bp['medians'][i]
    medianX = []
    medianY = []
    for j in range(2):
        medianX.append(med.get_xdata()[j])
        medianY.append(med.get_ydata()[j])
        plt.plot(medianX, medianY, 'k')
        medians[i] = medianY[0]

    plt.plot([np.average(med.get_xdata())], [np.average(data[i])],
             color='w', marker='*', markeredgecolor='k')

plt.figtext(0.60, 0.18,  'no. of addresses in aggrS',
            backgroundcolor=boxColors[1], color='black', weight='roman', size='x-small')
plt.figtext(0.60, 0.145, 'no. of addresses in edgeS',
            backgroundcolor=boxColors[2], color='white', weight='roman', size='x-small')
plt.figtext(0.60, 0.110, '*', color='white', backgroundcolor='silver',
            weight='roman', size='medium')
plt.figtext(0.62, 0.113, 'average value', color='black', weight='roman', size='x-small')

plt.show()
