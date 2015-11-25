spList, Q, v = findMeetingPoint(points, robots, robotV)

orig = np.array([spList[v[0]].x[v[1]],spList[v[0]].z[v[1]],spList[v[0]].z[v[1]]]

def findParent(number,robot):
    sp = int(number)/1000
    n = number - sp*1000
    child = spList[sp].parent[n][robot]
    x = spList[sp].x[n]
    y = spList[sp].y[n]
    z = spList[sp].z[n]
    print child
#    findParent(child,robot)
    return child, x, y, z
    

x = spList[v[0]].x[v[1]]   
y = spList[v[0]].y[v[1]]   
z = spList[v[0]].z[v[1]]     
xPlot=[[x],[x],[x],[x]]   
yPlot=[[y],[y],[y],[y]]
zPlot=[[z],[z],[z],[z]]  
for robot,parent in enumerate(spList[v[0]].parent[v[1]]):
    child, x, y, z = findParent(parent,robot)
    xPlot[robot].append(x)
    yPlot[robot].append(y)
    zPlot[robot].append(z)
    while child > 0:
        child, x, y, z = findParent(child,robot)
        xPlot[robot].append(x)
        yPlot[robot].append(y)
        zPlot[robot].append(z)
fig = plt.figure(7)
ax = fig.gca(projection='3d')
ax.plot(xPlot[0], yPlot[0], zPlot[0],'r-')
ax.plot(xPlot[1], yPlot[1], zPlot[1],'b-')
ax.plot(xPlot[2], yPlot[2], zPlot[2],'m-')
ax.plot(xPlot[3], yPlot[3], zPlot[3],'g-')
plt.show(block=False) 
        
        
        
        
