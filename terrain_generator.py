'''
Input: A set P of n+1 points with assigned heights
Output: A triangulated terrain map with edges that are functions of x and y
'''

import numpy as np
import matplotlib.pyplot as plt

points = np.array([(3, 9, 4),(3, 18, 2),(6, 30, 10),(12, 42, 2),(15, 9, 0),(15, 42, 1),(21, 21, 5),(32, 33, 0),(35, 24, 2),(35, 51, 7),(47, 30, 1)])

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
                for s in T:
                    plt.plot([s[0],s[2],s[4],s[0]],[s[1],s[3],s[5],s[1]])
                plt.axis([0, 50, 0, 60])
                plt.show(block=False)

                
#            for v in range[3]:t 
#                if pointOnLine(r, [t[v], t[(v+1)%3]]):
#                    t1 = legalizeEdge(r, t[(v+2)%3],  t[v])
#                    t2 = legalizeEdge(r, t[(v+1)%3], t[(v+2)%3])
#                    T = np.delete(T, i, 1)
#                    T = np.c_[T,t1]
#                    T = np.c_[T,t2]                    

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
            edgeList = np.delete(edgeList,indOpp[0][0],0)
#            edgeList = np.delete(edgeList,indCurr[0][0],0)         
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
    
def legal(pi,pj,pk,pr):
    if ((pi[0]-pj[0])**2 + (pi[1]-pj[1])**2) > ((pk[0]-pr[0])**2 + (pk[1]-pr[1])**2):
        if not(line_intersect([pi,pj],[pk,pr])):
            return True
        else:
            return False
    else:
        return True

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
    
def pointOnLine(p, l):
    return (check_turn_dir(p, [l[0], l[1]], [l[2], l[3]]) == 0)

def pointInTriangle(p, t):
    if all(r == t[0:2]) or all(r == t[2:4]) or all(r == t[4:6]):
        return False
    else:
        b1 = check_turn_dir(p, [t[0],t[1]], [t[2],t[3]]) < 0
        b2 = check_turn_dir(p, [t[2],t[3]], [t[4],t[5]]) < 0
        b3 = check_turn_dir(p, [t[4],t[5]], [t[0],t[1]]) < 0
        return ((b1 == b2) & (b2 == b3))

def check_turn_dir(p1,p2,p3):
    seg1 = [a - b for a,b in zip(p2,p1)]
    seg2 = [a - b for a,b in zip(p3,p2)]
    dir = np.cross(seg1,seg2)
    return dir
    
if __name__ == '__main__':
    DelaunayTri(points)
