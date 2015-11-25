import copy
import numpy as np
from Djikstra import index_2d, weightedCost

def test(spList, Q):        
    indices = sorted(range(len(Q[2])), key=Q[2].__getitem__)
    Q[0] = [y for (y,x) in sorted(zip(Q[0],Q[2]), key=lambda pair: pair[1])]
    Q[1] = [y for (y,x) in sorted(zip(Q[1],Q[2]), key=lambda pair: pair[1])]
    Q[3] = [y for (y,x) in sorted(zip(Q[3],Q[2]), key=lambda pair: pair[1])]
    Q[2] = [y for (y,x) in sorted(zip(Q[2],Q[2]), key=lambda pair: pair[1])]
    v = [Q[0].pop(0),Q[1].pop(0),Q[2].pop(0),Q[3].pop(0)]
    minCostInd = v[3] # spList[v[0]].localheap[v[1]][0]
    costV = spList[v[0]].costs[v[1]][minCostInd]
    print spList[v[0]].localheap[v[1]]
    spList[v[0]].localheap[v[1]] = np.delete(spList[v[0]].localheap[v[1]],0)
#        print v, minCostInd, costV, spList[v[0]].localheap[v[1]], len(Q[0])
#        print spList[v[0]].x[v[1]], spList[v[0]].y[v[1]]
    print v, minCostInd, spList[v[0]].localheap[v[1]]
    if (spList[v[0]].localheap[v[1]].size == 0):
        print "Reached goal!", v
    zip(Q[0],Q[1],Q[2],Q[3])
    adjList = [[],[]]
    for i,sn in enumerate(spList):
        vRet = index_2d(sn,[spList[v[0]].x[v[1]],spList[v[0]].y[v[1]]])
        if len(vRet) > 0:
            adjList[0].append(vRet)
            adjList[1].append([i]*len(vRet))
    adjList = [[item for sublist in adjList[0] for item in sublist],[item for sublist in adjList[1] for item in sublist]]
    for vn,sn in zip(adjList[0],adjList[1]):
#            print spList[sn].x[vn], spList[sn].y[vn]
        costU = spList[sn].costs[vn][minCostInd]
        if costU > (costV + weightedCost([spList[sn].x[vn],spList[sn].y[vn],spList[sn].z[vn]],[spList[v[0]].x[v[1]],spList[v[0]].y[v[1]],spList[v[0]].z[v[1]]])):
            spList[sn].costs[vn][minCostInd] = (costV + weightedCost([spList[sn].x[vn],spList[sn].y[vn],spList[sn].z[vn]],[spList[v[0]].x[v[1]],spList[v[0]].y[v[1]],spList[v[0]].z[v[1]]]))
            spList[sn].parent[vn][minCostInd] = v[0]*1000 + v[1]
#            for t in range(len(spList[sn].localheap[vn])):
#                spList[sn].localheap[vn][t] = spList[sn].costs[vn][spList[sn].localheap[vn][t]]
            order = spList[sn].costs[vn].argsort()
            print order
            print sn, vn
            print spList[sn].localheap[vn]
            t = 0
            orig = copy.copy(spList[sn].localheap[vn])
            for o in order:
                if o in orig:
                    spList[sn].localheap[vn][t] = o 
                    t += 1
            print spList[sn].localheap[vn]
#            spList[sn].localheap[vn] = spList[sn].costs[vn].argsort()
            if minCostInd == spList[sn].localheap[vn][0]:
#                    print "adjusted", spList[sn].x[vn], spList[sn].y[vn]
                Qs = [i for i, x in enumerate(Q[0]) if x == sn]
                Qv = [i for i, x in enumerate(Q[1]) if x == vn]
                Qr = [i for i, x in enumerate(Q[3]) if x == minCostInd]
                print sn, vn
                if len(set(Qs).intersection(Qv,Qr)) > 0:
                    index = set(Qs).intersection(Qv,Qr).pop()
                    Q[2][index] = spList[sn].costs[vn][minCostInd]
#        print spList[0].costs, spList[1].costs
#        zip(Q[0],Q[1],Q[2])
    print len(Q[0])
    return spList, Q
    
#    for i in range(len(Q[0])):
#        ss, Qs = test(ss,Qs)

H = copy.copy(Q)
for h in H[2]:
    if h > 5000:
        h = 50   
pylab.plot(range(len(Q[0])),H[0],'--b')
pylab.plot(range(len(Q[0])),H[1],'.r')
pylab.plot(range(len(Q[0])),H[2],'-g')
pylab.plot(range(len(Q[0])),H[3],'-.m')

pylab.plot(range(len(spList[1].costs[:,1])),spList[1].costs[:,1],'.r')

pylab.show(block=False)


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(spList[1].x, spList[1].y, spList[1].costs[:,1],'b.')
ax.plot(spList[0].x, spList[0].y, spList[0].costs[:,1],'r.')
ax.plot(spList[1].x, spList[1].y, spList[1].costs[:,0],'g.')
ax.plot(spList[0].x, spList[0].y, spList[0].costs[:,0],'c.')
plt.show(block=False)




                
