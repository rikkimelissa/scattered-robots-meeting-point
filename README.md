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
- Here's an image: 
- ![text](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p11.png) ![text2](https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p12.png)
<img src="https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p11.png" style="float: left; width: 30%; margin-right: 1%; margin-bottom: 0.5em;">
<img src="https://raw.githubusercontent.com/rikkimelissa/scattered-robots-meeting-point/master/src/p12.png" style="float: left; width: 30%; margin-right: 1%; margin-bottom: 0.5em;">
<p style="clear: both;">

## Known issues ##
- The Delaunay triangulation has issues sometimes if three points lie on a straight line.
- Djikstra's algorithm will occasionally not return a meeting point.

