import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from G_construction import construct_G
from terrain_generator import terrain
from math import sqrt
import copy

points = np.array([(3, 9, 4),(3, 18, 2),(6, 30, 4),(12, 42, 2),(15, 9, 0),(15, 42, 1),(21, 21, 5),(32, 33, 0),(35, 24, 2),(35, 51, 3),(47, 30, 1),(2,1,5),(40,2,3),(7,16,2),(25,10,1)])
robots = [1,6,17,20]
points = np.array([(3, 9, 4),(3, 18, 2),(6, 30, 4),(12, 42, 2)])
robotsS = [0,1]
robotV = [1,0]

def findMeetingPoint(points, robots):
    spList, Q = initialize(points, robotsS, robotV) 
#        indices = [i for i, x in enumerate(Q[2]) if x == 0]
    while True:      
        Q[0] = [y for (y,x) in sorted(zip(Q[0],Q[2]), key=lambda pair: pair[1])]
        Q[1] = [y for (y,x) in sorted(zip(Q[1],Q[2]), key=lambda pair: pair[1])]
        Q[3] = [y for (y,x) in sorted(zip(Q[3],Q[2]), key=lambda pair: pair[1])]
        Q[2] = [y for (y,x) in sorted(zip(Q[2],Q[2]), key=lambda pair: pair[1])]
        v = [Q[0].pop(0),Q[1].pop(0),Q[2].pop(0),Q[3].pop(0)]
        minCostInd = v[3]
        costV = spList[v[0]].costs[v[1]][minCostInd]
        spList[v[0]].localheap[v[1]] = np.delete(spList[v[0]].localheap[v[1]],0)
        if (spList[v[0]].localheap[v[1]].size == 0):
            print "Reached goal!", v
            break
        zip(Q[0],Q[1],Q[2],Q[3])
        adjList = [[],[]]
        for i,sn in enumerate(spList):
            vRet = index_2d(sn,[spList[v[0]].x[v[1]],spList[v[0]].y[v[1]]])
            if len(vRet) > 0:
                adjList[0].append(vRet)
                adjList[1].append([i]*len(vRet))
        adjList = [[item for sublist in adjList[0] for item in sublist],[item for sublist in adjList[1] for item in sublist]]
        for vn,sn in zip(adjList[0],adjList[1]):
            costU = spList[sn].costs[vn][minCostInd]
            if costU > (costV + weightedCost([spList[sn].x[vn],spList[sn].y[vn],spList[sn].z[vn]],[spList[v[0]].x[v[1]],spList[v[0]].y[v[1]],spList[v[0]].z[v[1]]])):
                spList[sn].costs[vn][minCostInd] = (costV + weightedCost([spList[sn].x[vn],spList[sn].y[vn],spList[sn].z[vn]],[spList[v[0]].x[v[1]],spList[v[0]].y[v[1]],spList[v[0]].z[v[1]]]))
                spList[sn].parent[vn][minCostInd] = v[0]*1000 + v[1]
                order = spList[sn].costs[vn].argsort()
                t = 0
                orig = copy.copy(spList[sn].localheap[vn])
                for o in order:
                    if o in orig:
                        spList[sn].localheap[vn][t] = o 
                        t += 1
                if minCostInd == spList[sn].localheap[vn][0]:
                    Qs = [i for i, x in enumerate(Q[0]) if x == sn]
                    Qv = [i for i, x in enumerate(Q[1]) if x == vn]
                    Qr = [i for i, x in enumerate(Q[3]) if x == minCostInd]
                    if len(set(Qs).intersection(Qv,Qr)) > 0:
                        index = set(Qs).intersection(Qv,Qr).pop()
                        Q[2][index] = spList[sn].costs[vn][minCostInd] 
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(spList[1].x, spList[1].y, spList[1].costs[:,1],'b.')
    ax.plot(spList[0].x, spList[0].y, spList[0].costs[:,1],'r.')
    ax.plot(spList[1].x, spList[1].y, spList[1].costs[:,0],'g.')
    ax.plot(spList[0].x, spList[0].y, spList[0].costs[:,0],'c.')
    plt.show(block=False)    
    return spList, Q, v            


find = lambda searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]

def initialize(points, robotsS, robotV):
    plt.close('all')
    t = terrain(points)
    spList = construct_G(t)
    s = len(robotsS)
    vn = spList[0].x.shape[0]
    Q = [[],[],[],[]]
    for sn, sp in enumerate(spList):
        sp.costs = np.empty([sp.x.shape[0],s])
        sp.parent = np.empty([sp.x.shape[0],s])
        sp.localheap = []
        for i in range(sp.x.shape[0]):
            sp.localheap.append([])
        for v in range(sp.x.shape[0]):
            for i in range(s):
                sp.costs[v,i] = float("inf")
                sp.parent[v,i] = float("nan")
                sp.localheap[v].append(i)
            #top = sp.costs[v].argmin()
#                minCostInd = sp.costs[v].argmin() #sp.localheap[v]
                Q[0].append(sn)
                Q[1].append(v)
                Q[2].append(float("inf"))
                Q[3].append(i)
    for i,r in enumerate(robotsS):
        sp = spList[r]
        sp.costs[robotV[i],i] = 0
        minCostInd = i
        sp.localheap[robotV[i]] = sp.costs[robotV[i]].argsort()
        Q[2][(vn*r + robotV[i])*s+i] = 0
    return spList, Q
        
def index_2d(myList, v):
    indRet = []
    for i, x in enumerate(myList.edge):
        if v[0] in x and v[1] in x:
            if (x.index(v[0]) == 0 and x.index(v[1]) == 1) or (x.index(v[0]) == 3 and x.index(v[1]) == 4):
                indX = np.where(myList.x == myList.edge[i][(x.index(v[0])+3)%6])
                indY = np.where(myList.y == myList.edge[i][(x.index(v[0])+4)%6])
                ind = np.intersect1d(indX[0],indY[0])[0]
                indRet.append(ind)
    return indRet  

def weightedCost(v,u):
    return sqrt((v[0] - u[0])**2 + (v[1] - u[1])**2 + (v[2] - u[2])**2)
    

if __name__ == '__main__':
    initialize(points, robotsS, robotV)
