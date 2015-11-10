#!/usr/bin/env python

'''
Input: A set P of n+1 points with assigned heights
Output: A triangulated terrain map with edges that are functions of x and y
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

points = np.array([(3, 9, 4),(3, 18, 2),(6, 30, 10),(12, 42, 2),(15, 9, 0),(15, 42, 1),(21, 21, 5),(32, 33, 0),(35, 24, 2),(35, 51, 7),(47, 30, 1),(2,1,8),(40,2,7),(7,16,2),(25,10,1)])

def terrain(p):

    # Calculate the Delaunay triangulation and return the triangles and the edge diagram
    tri, edgeList = DelaunayTri(p)
    plt.cla()
    for s in tri:
        plt.plot([s[0],s[2],s[4],s[0]],[s[1],s[3],s[5],s[1]])
    plt.axis([0, 50, 0, 60])
    plt.show(block=False) 
    
    # Calculate the slope equations for each triangle and return as a list with order: [x1, y1, x2, y2, x3, y3, norm[1], norm[2], norm[3], d]
    terrainList = np.array([[0,0,0,0,0,0,0,0,0,0]])
    for t in tri:
        terrainList = defineEquations(t, p, terrainList)
    terrainList = np.delete(terrainList,0,0)
          
    px = p[:,0]
    py = p[:,1]
    pz = p[:,2]
    xRange =  [a+(min(px)-2) for a in range(max(px)-min(px)+4)]
    yRange =  [a+(min(py)-2) for a in range(max(py)-min(py)+4)]    
    xx, yy = np.meshgrid(xRange,yRange)
    #zz = (-norm[0]*xx - norm[1]*yy - d)*1./norm[2]
    
    # Plot the terrain
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(px, py, pz, cmap=cm.jet, linewidth=0.2)
    plt.show(block=False)
    return terrainList

# Find the index of each triangle on the list of points and assign correct z height, then return the list of triangles with its associated height equation
def defineEquations(t, p, terrainList):
    u = np.array([t[0],t[1]])
    v = np.array([t[2],t[3]])
    w = np.array([t[4],t[5]])
    
    a = np.where(p[:,0]==u[0])[0]
    b = np.where(p[:,1]==u[1])[0]
    ind = np.intersect1d(a,b)[0]
    z = p[ind][2]
    u = np.concatenate((u,[z]))
    
    a = np.where(p[:,0]==v[0])[0]
    b = np.where(p[:,1]==v[1])[0]
    ind = np.intersect1d(a,b)[0]
    z = p[ind][2]
    v = np.concatenate((v,[z]))
    
    a = np.where(p[:,0]==w[0])[0]
    b = np.where(p[:,1]==w[1])[0]
    ind = np.intersect1d(a,b)[0]
    z = p[ind][2]
    w = np.concatenate((w,[z]))
    
    norm, d = definePlane(u,v,w)
    f = np.concatenate((t,norm,[d]))
    terrainList = np.concatenate((terrainList,[f]),axis=0)
    return terrainList

# Use the height of the triangles to calculate the equations of each 3D triangle   
def definePlane(p,q,r):
    v1 = q-p
    v2 = r-p
    norm = np.cross(v1,v2)
    d = -np.sum(p*norm)     
    return norm, d
    
def DelaunayTri(p):
    px = p[:,0]
    py = p[:,1]
    # Set p0 to be the rightmost point
    p0 = [px[np.argmax(px)],py[np.argmax(px)]]
    # Remove this p0 from list of points
    np.delete(p,np.argmax(px),0)
    # Define two additional points such that P is contained in the triangle of these 3 points
    p1neg = [p0[0]-10000,p0[1]-100000]
    p2neg = [p0[0]-10000,p0[1]+100000]
    plt.scatter(px,py)
    plt.plot([p0[0],p1neg[0],p2neg[0],p0[0]],[p0[1],p1neg[1],p2neg[1],p0[1]])
    plt.show(block=False)
    # Initialize T with this single triangle
    t1 = [np.concatenate((p0,p2neg,p1neg))]
    t2 = [np.concatenate((p2neg,p1neg,p0))]
    t3 = [np.concatenate((p1neg,p0,p2neg))]
    edgeList = np.concatenate((t1,t2,t3))
    T = t1
    # Compute a random permutation of the rest of the points
    np.random.shuffle(p)
    for r3 in p:
        r = r3[0:2]
        for i,t in enumerate(T):
            # If the point is in the triangle, calculate the legal edges of the 3 new triangles and add these triangles and their edges to the lists
            if pointInTriangle(r, t):              
                t1, edgeList = legalizeEdge(r,[t[0],t[1]],[t[2],t[3]],edgeList)
                t2, edgeList = legalizeEdge(r,[t[2],t[3]],[t[4],t[5]],edgeList)
                t3, edgeList = legalizeEdge(r,[t[4],t[5]],[t[0],t[1]],edgeList)              
                T = np.concatenate((T,t1),axis=0)
                T = np.concatenate((T,t2),axis=0)
                T = np.concatenate((T,t3),axis=0)
                T = np.delete(T, i, 0)
                T = np.array([x for x in set(tuple(x) for x in T) & set(tuple(x) for x in edgeList)])
                plt.cla()
    Th = T
    nT = T.shape[0]  
    for i,tri in enumerate(T[::-1]):
        if (np.intersect1d(tri,p1neg)).size > 0 or (np.intersect1d(tri,p2neg)).size > 0:
            Th = np.delete(Th,nT-i-1,0)         
    return Th, edgeList             

# This functions legalizes all the edges. If for a given edge, the intersecting edge that could be drawn is shorter than the given edge, replace this edge with the intersecting edge. Recursive function
def legalizeEdge(pr, pi, pj, edgeList):
    indOpp = np.where((edgeList[:,0:4]==np.concatenate((pj, pi))).all(axis=1))
    indCurr = np.where((edgeList[:,0:4]==np.concatenate((pi, pj))).all(axis=1))
    if all(indOpp):
        pk = edgeList[indOpp[0][0]][4:6]
        if legal(pi, pj, pk, pr):
            edgeList[indCurr[0][0]][4:6] = pr
            e1 = np.concatenate((pr, pi, pj))
            e2 = np.concatenate((pj, pr, pi))
            edgeList = np.concatenate((edgeList,[e1],[e2]),axis=0)
            tri = [np.concatenate((pr, pi, pj))]
        else:
            edgeList[indCurr[0][0]][4:6] = pr
            edgeList = np.delete(edgeList,indOpp[0][0],0)       
            tri1, edgeList = legalizeEdge(pr, pi, pk, edgeList)
            tri2, edgeList = legalizeEdge(pr, pk, pj, edgeList)
            tri = np.concatenate((tri1,tri2),axis=0)
    else:
        edgeList[indCurr[0][0]][4:6] = pr
        e1 = np.concatenate((pr, pi, pj))
        e2 = np.concatenate((pj, pr, pi))
        edgeList = np.concatenate((edgeList,[e1],[e2]),axis=0)
        tri = [np.concatenate((pr, pi, pj))]
    return tri, edgeList

# Defines if a given edge is legal
def legal(pi,pj,pk,pr):
    if ((pi[0]-pj[0])**2 + (pi[1]-pj[1])**2) > ((pk[0]-pr[0])**2 + (pk[1]-pr[1])**2):
        if not(line_intersect([pi,pj],[pk,pr])):
            return True
        else:
            return False
    else:
        return True

# Checks for line intersection
def line_intersect(l1,l2):
# http://www.ahinson.com/algorithms_general/Sections/Geometry/ParametricLineIntersection.pdf
    x1 = l1[0][0]
    y1 = l1[0][1]
    x2 = l1[1][0]
    y2 = l1[1][1]
    x3 = l2[0][0]
    y3 = l2[0][1]
    x4 = l2[1][0]
    y4 = l2[1][1]
    s = float((x4-x3)*(y3-y1) - (x3-x1)*(y4-y3))/((x4-x3)*(y2-y1) - (x2-x1)*(y4-y3))
    t = float((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))/((x4-x3)*(y2-y1) - (x2-x1)*(y4-y3))
    if (s>=0 and s<=1 and t>=0 and t<=1):
        x_int = x1 + (x2-x1)*s
        y_int = y1 + (y2-y1)*s
        intersect = True
    else:
        intersect = False
        x_int = False
        y_int = False
    return intersect
    
# Checks if three points lie on a straight line
def pointOnLine(p, l):
    if (check_turn_dir(p, [l[0], l[1]], [l[2], l[3]]) == 0):
        return True
    else:
        return False

# Checks if a point is inside a triangle
def pointInTriangle(p, t):
    if all(p == t[0:2]) or all(p == t[2:4]) or all(p == t[4:6]):
        return False
    else:
        b1 = check_turn_dir(p, [t[0],t[1]], [t[2],t[3]]) < 0
        b2 = check_turn_dir(p, [t[2],t[3]], [t[4],t[5]]) < 0
        b3 = check_turn_dir(p, [t[4],t[5]], [t[0],t[1]]) < 0
        return ((b1 == b2) & (b2 == b3))

# Checks the turn direction for 3 points
def check_turn_dir(p1,p2,p3):
    seg1 = [a - b for a,b in zip(p2,p1)]
    seg2 = [a - b for a,b in zip(p3,p2)]
    dir = np.cross(seg1,seg2)
    return dir
    
if __name__ == '__main__':
    terrain(points)
