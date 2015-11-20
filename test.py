    
    
def test(spList, Q):        
    indices = sorted(range(len(Q[2])), key=Q[2].__getitem__)
    Q[0] = [y for (y,x) in sorted(zip(Q[0],Q[2]), key=lambda pair: pair[1])]
    Q[1] = [y for (y,x) in sorted(zip(Q[1],Q[2]), key=lambda pair: pair[1])]
    Q[2] = [y for (y,x) in sorted(zip(Q[2],Q[2]), key=lambda pair: pair[1])]
    v = [Q[0].pop(0),Q[1].pop(0),Q[2].pop(0)]
    minCostInd = spList[v[0]].localheap[v[1]][0]
    costV = spList[v[0]].costs[v[1]][minCostInd]
    print spList[v[0]].localheap[v[1]]
    spList[v[0]].localheap[v[1]] = np.delete(spList[v[0]].localheap[v[1]],0)
#        print v, minCostInd, costV, spList[v[0]].localheap[v[1]], len(Q[0])
#        print spList[v[0]].x[v[1]], spList[v[0]].y[v[1]]
    print v, minCostInd, spList[v[0]].localheap[v[1]]
    if (spList[v[0]].localheap[v[1]].size == 0):
        print "Reached goal!", v
    zip(Q[0],Q[1],Q[2])
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
            t = 0
            for o in order:
                if o in spList[sn].localheap[vn]:
                    spList[sn].localheap[vn][t] = o 
                    t += 1
#            spList[sn].localheap[vn] = spList[sn].costs[vn].argsort()
            if minCostInd == spList[sn].localheap[vn][0]:
#                    print "adjusted", spList[sn].x[vn], spList[sn].y[vn]
                Qs = [i for i, x in enumerate(Q[0]) if x == sn]
                Qv = [i for i, x in enumerate(Q[1]) if x == vn]
                print sn, vn
                index = set(Qs).intersection(Qv).pop()
                Q[2][index] = spList[sn].costs[vn][minCostInd]
#        print spList[0].costs, spList[1].costs
#        zip(Q[0],Q[1],Q[2])
    print len(Q[0])
    return spList, Q

                
