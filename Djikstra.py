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
    for sn, sp in enumerate(spList):
        sp.costs = np.empty([range(s),range(sp.x)])
        sp.parents = np.empty([range(s),range(sp.x)]) 
        for v in range(sp.x):
            for i in range(s):
                sp.costs[i,v] = float("inf")
                sp.parent[i,v] = float("nan")
                sp.localheap.append(i)
        top =  np.unravel_index(sp.costs.argmin(),sp.costs.shape)[0]
        minCostInd = sp.localheap.pop(top)
        Q[0].append(sn)
        Q[1].append(v)
        Q[2].append(sp.costs.min())
    
    
        





if __name__ == '__main__':
    findMeetingPoint(points, robots)
