#!/usr/bin/env python

'''
Input: A list of triangles
Output: A list of triangles with added vertices and edges
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from terrain_generator import terrain

t2 = np.array([[   25,    10,    21,    21,    15,     9,    -7,   -44,   114,  -501],
       [   32,    33,    35,    24,    47,    30,    -3,    27,   126, 795],
       [   25,    10,    15,     9,     2,     1,   -16,    93,    67, 597],
       [    3,     9,     2,     1,    15,     9,    32,    44,    96, 876],
       [    3,     9,    15,     9,     7,    16,    28,     8,    84, 492],
       [    3,     9,     7,    16,     3,    18,     4,     8,    36, 228],
       [   40,     2,    47,    30,    35,    24,    -8,    65,   294, 1868],
       [    7,    16,    15,     9,    21,    21,   -11,   -52,   138,  -633],
       [    7,    16,    21,    21,     6,    30,    -2,  -115,   201, -1452],
       [   21,    21,    15,    42,     6,    30,   141,    90,   261, 6156],
       [   25,    10,    40,     2,    35,    24,   -92,    45,   290, -1560],
       [   15,    42,    32,    33,    35,    51,   -45,  -122,   333, -5466],
       [   21,    21,    35,    24,    32,    33,    21,    37,   135, 1893],
       [   12,    42,     6,    30,    15,    42,    12,    18,    36, 972],
       [    3,     9,     3,    18,     2,     1,    20,     2,     9, 114],
       [   12,    42,    15,    42,    35,    51,     9,   -38,    27, -1434],
       [   25,    10,     2,     1,    40,     2,     2,   243,   319, 2799],
       [    3,    18,     7,    16,     6,    30,   -16,   -32,    54,  -516],
       [   21,    21,    32,    33,    15,    42,    57,    74,   303, 4266],
       [   35,    51,    32,    33,    47,    30,   -39,  -102,   279, -4614],
       [   25,    10,    35,    24,    21,    21,    45,   -44,   166, 851]])
       

points = np.array([(3, 9, 4),(3, 18, 2),(6, 30, 4),(12, 42, 2),(15, 9, 0),(15, 42, 1),(21, 21, 5),(32, 33, 0),(35, 24, 2),(35, 51, 3),(47, 30, 1),(2,1,5),(40,2,3),(7,16,2),(25,10,1)])

def demo(points):
    t = terrain(points)
    construct_G(t)
     
def construct_G(terrain):

    spList = []
    
    # Calculate Steiner points
    for tri in terrain:
        sp = steiner_points()
        sp = add_Steiners(tri,sp)        
        sp.x = np.delete(sp.x,0)
        sp.y = np.delete(sp.y,0)
        sp.z = np.delete(sp.z,0)
        spList.append(sp)
        sp.edge = []
    
    # Plot Steiner points
    fig = plt.figure(3)
    ax = fig.gca(projection='3d')
    for sp in spList:
        ax.scatter(sp.x, sp.y, sp.z)
    plt.title('Triangulation plotted with Steiner points')
    plt.show(block=False)
    
    # Calculate Steiner edges
    spList = connect_vertices(spList)

    # Plot Steiner edges   
    fig = plt.figure(4)       
    ax = fig.gca(projection='3d') 
    sp = spList[0]  
    for edge in sp.edge:
        ax.plot([edge[0],edge[3]],[edge[1],edge[4]],[edge[2],edge[5]])
    plt.title('Example of Steiner edge generation')
    plt.show(block=False)
    return spList

# Add edges between all Steiner points
def connect_vertices(spList):
    m = spList[0].x.shape[0]/3-1
    for i,sp in enumerate(spList):
    
        # Chain points
        for j in range(3):
            xo, yo, zo = [sp.x[j], sp.y[j], sp.z[j]]
            for k in range(10):
                xd, yd, zd = [sp.x[j*m+3+k],sp.y[j*m+3+k],sp.z[j*m+3+k]]
                edge = [xo, yo, zo, xd, yd, zd]
                spList[i].edge.append(edge)  
                xo = xd
                yo = yd
                zo = zd
            xd, yd, zd = [sp.x[(j+1)%3], sp.y[(j+1)%3], sp.z[(j+1)%3]]
            edge = [xo, yo, zo, xd, yd, zd]
            spList[i].edge.append(edge) 
                
        # Vertex-steiner point edges  
        xo, yo, zo = [sp.x[1], sp.y[1], sp.z[1]] 
        for xd, yd, zd in zip(sp.x[2*m+3:],sp.y[2*m+3:],sp.z[2*m+3:]):
            edge = [xo, yo, zo, xd, yd, zd]
            spList[i].edge.append(edge)     
        xo, yo, zo = [sp.x[2], sp.y[2], sp.z[2]] 
        for xd, yd, zd in zip(sp.x[3:m+3],sp.y[3:m+3],sp.z[3:m+3]):
            edge = [xo, yo, zo, xd, yd, zd]
            spList[i].edge.append(edge)  
        xo, yo, zo = [sp.x[0], sp.y[0], sp.z[0]] 
        for xd, yd, zd in zip(sp.x[m+3:2*m+3],sp.y[m+3:2*m+3],sp.z[m+3:2*m+3]):
            edge = [xo, yo, zo, xd, yd, zd]
            spList[i].edge.append(edge) 
                
        # Steiner point-steiner point edges
        for xo, yo, zo in zip(sp.x[3:m+3], sp.y[3:m+3], sp.z[3:m+3]):
            for xd, yd, zd in zip(sp.x[m+3:],sp.y[m+3:],sp.z[m+3:]):
                edge = [xo, yo, zo, xd, yd, zd]
                spList[i].edge.append(edge)
        for xo, yo, zo in zip(sp.x[2*m+3:], sp.y[2*m+3:], sp.z[2*m+3:]):
            for xd, yd, zd in zip(sp.x[m+3:2*m+3],sp.y[m+3:2*m+3],sp.z[m+3:2*m+3]):
                edge = [xo, yo, zo, xd, yd, zd]
                spList[i].edge.append(edge)              
    return spList
        

class steiner_points:
    x = np.array([0])
    y = np.array([0])
    z = np.array([0])
    edge = []
    costs = []
    parent = []
    localheap = []

# Add Steiner points
def add_Steiners(tri, sp, m=10):

    # Calculate the equation of the plane
    u = np.array([tri[0],tri[1]])
    v = np.array([tri[2],tri[3]])
    w = np.array([tri[4],tri[5]])
    norm = np.array([tri[6],tri[7],tri[8]])
    d = tri[9]
    
    sp.x = np.append(sp.x,[u[0],v[0],w[0]])
    sp.y = np.append(sp.y,[u[1],v[1],w[1]])
    uz = float(d - norm[0]*u[0] - norm[1]*u[1])/norm[2]
    vz = float(d - norm[0]*v[0] - norm[1]*v[1])/norm[2]
    wz = float(d - norm[0]*w[0] - norm[1]*w[1])/norm[2]
    sp.z = np.append(sp.z,[uz,vz,wz])
    
    # Place Steiner points for one edge at a time
    for i in range(m):
        xd,yd = ((v-u)/float(m+1))
        x,y = np.round(u + (i+1)*np.array([xd,yd]),4)
        z = np.round(float(d - norm[0]*x - norm[1]*y)/norm[2],4)
        sp.x = np.append(sp.x,x)
        sp.y = np.append(sp.y,y)
        sp.z = np.append(sp.z,z)
        
    for i in range(m):
        xd,yd = ((w-v)/float(m+1))
        x,y = np.round(v + (i+1)*np.array([xd,yd]),4)
        z = np.round(float(d - norm[0]*x - norm[1]*y)/norm[2],4)
        sp.x = np.append(sp.x,x)
        sp.y = np.append(sp.y,y)
        sp.z = np.append(sp.z,z)
        
    for i in range(m):
        xd,yd = ((u-w)/float(m+1))
        x,y = np.round(w + (i+1)*np.array([xd,yd]),4)
        z = np.round(float(d - norm[0]*x - norm[1]*y)/norm[2],4)
        sp.x = np.append(sp.x,x)
        sp.y = np.append(sp.y,y)
        sp.z = np.append(sp.z,z)

    return sp



if __name__ == '__main__':
    demo(points)
