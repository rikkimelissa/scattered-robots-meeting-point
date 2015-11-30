#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Djikstra import findMeetingPoint
from math import sqrt
import copy

#orig = np.array([spList[v[0]].x[v[1]],spList[v[0]].z[v[1]],spList[v[0]].z[v[1]]]    

points = np.array([(4, 8, 1),(3, 18, 2),(6, 35, 3),(12, 42, 2),(15, 9, 0),(15, 42, 1),(18, 25, 5),(32, 33, 0),(35, 24, 2),(35, 51, 1),(47, 30, 1),(2,1,0),(40,2,2),(7,16,3),(25,7,1),(48,21,1)])
robots = [1,6,17,20]
robotV = [1,0,2,0]

def plotPath(points, robots, robotV):
    spList, Q, v = findMeetingPoint(points, robots, robotV)
    x = spList[v[0]].x[v[1]]   
    y = spList[v[0]].y[v[1]]   
    z = spList[v[0]].z[v[1]]     
    xPlot=[[x],[x],[x],[x]]   
    yPlot=[[y],[y],[y],[y]]
    zPlot=[[z],[z],[z],[z]]  
    for robot,parent in enumerate(spList[v[0]].parent[v[1]]):
        if parent > 0:
            child, x, y, z = findParent(parent,robot,spList)
            xPlot[robot].append(x)
            yPlot[robot].append(y)
            zPlot[robot].append(z)
            while child > 0:
                child, x, y, z = findParent(child,robot,spList)
                xPlot[robot].append(x)
                yPlot[robot].append(y)
                zPlot[robot].append(z)
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    ax.plot(xPlot[0], yPlot[0], zPlot[0],linewidth=3.0,color='darkorchid')
    ax.plot(xPlot[1], yPlot[1], zPlot[1],linewidth=3.0,color='tomato')
    ax.plot(xPlot[2], yPlot[2], zPlot[2],linewidth=3.0,color='lime')
    ax.plot(xPlot[3], yPlot[3], zPlot[3],linewidth=3.0,color='yellow')
    ax.plot(xPlot[0][0], yPlot[0][0], zPlot[0][0])
    plt.show(block=False) 

    fig = plt.figure(2)
    ax = fig.gca()
    ax.plot(xPlot[0], yPlot[0],linewidth=3.0,color='darkorchid')
    ax.plot(xPlot[1], yPlot[1],linewidth=3.0,color='tomato')
    ax.plot(xPlot[2], yPlot[2],linewidth=3.0,color='lime')
    ax.plot(xPlot[3], yPlot[3],linewidth=3.0,color='yellow')
    ax.plot(xPlot[0][0], yPlot[0][0], '.',markersize=20, color='black')
    ax.plot(xPlot[0][-1], yPlot[0][-1], '.',markersize=20, color='darkorchid')
    ax.plot(xPlot[1][-1], yPlot[1][-1], '.',markersize=20, color='tomato')
    ax.plot(xPlot[2][-1], yPlot[2][-1], '.',markersize=20, color='lime') 
    ax.plot(xPlot[3][-1], yPlot[3][-1], '.',markersize=20, color='yellow')
    plt.show(block=False) 

def findParent(number,robot,spList):
    sp = int(number)/1000
    n = number - sp*1000
    child = spList[sp].parent[n][robot]
    x = spList[sp].x[n]
    y = spList[sp].y[n]
    z = spList[sp].z[n]
    print child
#    findParent(child,robot)
    return child, x, y, z   

if __name__ == '__main__':
    plotPath(points, robots, robotV)
#    x=1
        
        
        
