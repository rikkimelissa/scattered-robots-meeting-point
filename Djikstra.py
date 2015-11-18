import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from G_construction import construct_G
from terrain_generator import terrain

points = np.array([(3, 9, 4),(3, 18, 2),(6, 30, 4),(12, 42, 2),(15, 9, 0),(15, 42, 1),(21, 21, 5),(32, 33, 0),(35, 24, 2),(35, 51, 3),(47, 30, 1),(2,1,5),(40,2,3),(7,16,2),(25,10,1)])
robots = [1,6,17,20]

def findMeetingPoint(points, robots):
    plt.close('all')
    t = terrain(points)
    spList = construct_G(t)
    s = len(robots)
    vn = sp.x.shape[0]
    Q = [[],[],[]]
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
            minCostInd = sp.costs[v].argmin() #sp.localheap[v]
            Q[0].append(sn)
            Q[1].append(v)
            Q[2].append(sp.costs[v,minCostInd])
    for i,r in enumerate(robots):
        sp = spList[r]
        sp.costs[0,i] = 0
        minCostInd = i
        sp.localheap[0] = sp.costs[0].argsort()
        print vn,r
        Q[2][vn*r] = 0
#        indices = [i for i, x in enumerate(Q[2]) if x == 0]
    while True:
        indices = sorted(range(len(Q[2])), key=Q[2].__getitem__)
        Q[0] = [y for (y,x) in sorted(zip(Q[0],Q[2]), key=lambda pair: pair[1])]
        Q[1] = [y for (y,x) in sorted(zip(Q[1],Q[2]), key=lambda pair: pair[1])]
        Q[2] = [y for (y,x) in sorted(zip(Q[2],Q[2]), key=lambda pair: pair[1])]
        v = [Q[0].pop(0),Q[1].pop(0),Q[2].pop(0)]
        minCostInd = spList[v[0]].localheap[v[1]][0]
        costV = spList[v[0]].costs[v[1]][minCostInd]
        spList[v[0]].localheap[v[1]] = np.delete(spList[v[0]].localheap[v[1]],0)
        if (spList[v[0]].localheap[v[1]].size == 0):
            return v
             


        
    
    
        





if __name__ == '__main__':
    findMeetingPoint(points, robots)
