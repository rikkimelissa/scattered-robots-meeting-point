About this package
=================

This repository contains code to calculate the meeting point of scattered robots on weighted terrain surfaces. This code implements the algorithm detailed in [this paper](http://people.scs.carleton.ca/~lanthier/personal/cv/CATS2005_8.5x11.pdf) by Mark Lanthier, Doron Nussbaum, and Tsuo-Jung Wang.

## Package contents ##
This package contains four files:
- `terrain_generator` calculates the Delaunay triangulation for a set of points in 3D space based on the algorithm given in *Computational Geometry Algorithms and Applications* by Mark de Berg, et al. The triangulation is returned as a list of triangles and plotted using Python's matplotlib algorithm for contour and surf plotting.
- `G_construction` constructs of graph of Steiner points and edges at ten per edge of the original triangulation.
- `Djikstra` invokes a shortest path algorithm from each of the source vertices on which the robots are positioned. The algorithm is modified as a multiple-source single-target variation such that the algorithm stops at some vertex p' which is the approximating meeting point.
- `plot_path` traces the parents of the meeting point for each robot and plots the paths in two ways.

## Running this package ##
- The default run of the simulation can be launched by running `plot_path.py` from the python command line.
- The points used for triangulation can be changed at the top of the `plot_path` file, as can the locations of the robots, which are specified by their position in the triangle list.

## Results ##
- This section shows the results of the algorithms. First the triangulation is shown with Steiner points and an example of Steiner edges. Next, four examples of calculated meeting points are shown. The contour map is shown with the start locations of each robot displayed as a circle of the robot's color, each robot's path in a different color, and the calculated meeting point shown as a black circle. The paths are also plotted on the terrain map and shown from various angles.

- The triangulation with Steiner points added, from two angles:
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/sp1.png) ![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/sp2.png)
- An example of a terrain face with Steiner edges:
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/se1.png)
- Path to meeting point, example 1:
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p14.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p11.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p12.png)
- Path to meeting point, example 2:
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p21.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p22.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p23.png)
- Path to meeting point, example 3:
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p32.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p31.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p33.png)
- Path to meeting point, example 4:
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p42.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p41.png)
![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p43.png)

## Known issues ##
- The Delaunay triangulation has issues sometimes if three points lie on a straight line.
- Djikstra's algorithm will occasionally not return a meeting point.

