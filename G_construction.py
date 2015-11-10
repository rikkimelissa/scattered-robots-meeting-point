#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

terrain = np.array([[   25,    10,    21,    21,    15,     9,    -7,   -44,   114,  -501],
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
       [   21,    21,    32,    33,    15,    42,    57,    74,   303,4266],
       [   35,    51,    32,    33,    47,    30,   -39,  -102,   279, -4614],
       [   25,    10,    35,    24,    21,    21,    45,   -44,   166, 851]])
    
def construct_G(terrain):

    sp = steiner_points()
    
    for tri in terrain:
        sp = add_Steiners(tri,sp)        
    sp.x = np.delete(sp.x,0)
    sp.y = np.delete(sp.y,0)
    sp.z = np.delete(sp.z,0)
    sp.tri = np.delete(sp.tri,0)
    
    # Plot Steiner points
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(sp.x, sp.y, sp.z)
    plt.show(block=False)

def connect_vertices(sp):
    for N in sp.tri:
        

class steiner_points:
    x = np.array([0])
    y = np.array([0])
    z = np.array([0])
    tri = np.array([0])

def add_Steiners(tri, sp, m=10):
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
    
    for i in range(m):
        xd,yd = ((v-u)/float(m))
        x,y = u + (i+1)*np.array([xd,yd])
        z = float(d - norm[0]*x - norm[1]*y)/norm[2]
        sp.x = np.append(sp.x,x)
        sp.y = np.append(sp.y,y)
        sp.z = np.append(sp.z,z)
        
    for i in range(m):
        xd,yd = ((w-v)/float(m))
        x,y = v + (i+1)*np.array([xd,yd])
        z = float(d - norm[0]*x - norm[1]*y)/norm[2]
        sp.x = np.append(sp.x,x)
        sp.y = np.append(sp.y,y)
        sp.z = np.append(sp.z,z)
        
    for i in range(m):
        xd,yd = ((u-w)/float(m))
        x,y = w + (i+1)*np.array([xd,yd])
        z = float(d - norm[0]*x - norm[1]*y)/norm[2]
        sp.x = np.append(sp.x,x)
        sp.y = np.append(sp.y,y)
        sp.z = np.append(sp.z,z)
    
    prev = sp.tri[-1]
    sp.tri = np.append(sp.tri,(m+3)*[prev+1])
    return sp



if __name__ == '__main__':
    construct_G(terrain)
