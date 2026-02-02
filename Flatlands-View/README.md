# Flatlands View

## Overview

This project was inspired by [*Flatland: A Romance of Many Dimensions*](https://en.wikipedia.org/wiki/Flatland), a novella written by Edwin Abbott Abbott.

The book entails the story of a square who lives in a world called Flatland. Flatland is inhabited by 2-dimensional polygons, dubbed flatlanders.

As they are two dimensional, the flatlanders are only able to visually see one another as one dimensional line segments. However, they are able to identify one another through depth perception, allowing them to identify how many sides each person has.

This book inspired me to create a function in python that would create a visualisation to replicate how an inhabitant of Flatland would view other flatlanders. 

## Idea

The idea I came up with was for our regular polygon to have a center at the origin, whilst having a circumcircle with radius 1 unit. Then the $x = 1$ line could act as the 'observer'.

The plan was to then visualise what the $x = 1$ line 'saw' by calculate how far the shape was from the $x = 1$ line for every y value. In this case $y ∈ [-1,1]$. Then, we can calculate the distance from each coordinate on the visible side of the polygon, and translate it into some sort of heatmap that acts almost like contour lines, giving the perception of depth.

## Prerequisites

For these functions, naturally we will require the Numpy and Matplotlib packages in python. Numpy for arrays and numerical calculations, and Matplotlib for visualisation tools.

We will also import defaultdict from collections, which will help to reduce the number of calculations and iterations needed.

```python 
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
```
## Generate Polygon

For the first part of the visualisation, I would first have to create a function which constructs a regular n-sided polygon. First, we will have to find out the coordinates of the corners of the polygon.

We can use the fact that for regular polygons, the angle at the centre between two adjacent corners will be equal to $360°/n$. So, given one coordinate of the polygon, we can calculate the coordinates of the rest of the corners using trigonometry.

The code below repeats the (1,0) coordinate, as it will be useful for later.

```python 
def Generate_Polygon(n):
    """
    Generates and plots points of a n-sided polygon.
    n should be a positive integer.
    """
    #Create an array for the x and y coordinates of each point
    points = np.zeros((n+1,2))
    
    #Create the points for the polygon and add them to the array
    for i in range(n+1):
        points[i] = [np.cos(i*2*np.pi/n),np.sin(i*2*np.pi/n)]

    return points
```

For `Generate_Polygon(3)`, we obtain:

```python
array([[ 1.00000000e+00,  0.00000000e+00],
       [-5.00000000e-01,  8.66025404e-01],
       [-5.00000000e-01, -8.66025404e-01],
       [ 1.00000000e+00, -2.44929360e-16]])
```

For `Generate_Polygon(4)`:

```python 
array([[ 1.0000000e+00,  0.0000000e+00],
       [ 6.1232340e-17,  1.0000000e+00],
       [-1.0000000e+00,  1.2246468e-16],
       [-1.8369702e-16, -1.0000000e+00],
       [ 1.0000000e+00, -2.4492936e-16]])
```

And for `Generate_Polygon(5)`:

```python
array([[ 1.00000000e+00,  0.00000000e+00],
       [ 3.09016994e-01,  9.51056516e-01],
       [-8.09016994e-01,  5.87785252e-01],
       [-8.09016994e-01, -5.87785252e-01],
       [ 3.09016994e-01, -9.51056516e-01],
       [ 1.00000000e+00, -2.44929360e-16]])
```

## Generate Polygon Graph

This function essentially does the same thing as Generate Polygon, but generates a graph of the polygon on the 2-D plane.

```python 
def Generate_Polygon_Graph(n,theta=0):
    """
    Generates and plots points of a n-sided polygon.
    n should be a positive integer.
    theta should be an angle between 0 and 360 degrees.
    """
    #Create an array for the x and y coordinates of each point
    points = np.zeros((n,2))
    
    #Create the points for the polygon and add them to the array
    for i in range(n):
        points[i] = [np.cos(i*2*np.pi/n),np.sin(i*2*np.pi/n)]
    
    #Adjust for angle
    theta = theta*np.pi/180
        
    transformation = np.array([[np.cos(theta), -np.sin(theta)],
                               [np.sin(theta), np.cos(theta)]])
        
    points = np.dot(points,transformation)
    
    #Plot out the polygon
    polygon = plt.Polygon(points, closed=True, edgecolor='black', facecolor='lightblue')
    plt.gca().add_patch(polygon)
    
    #Set limits of the graph
    plt.xlim(-1.5,1.5)
    plt.ylim(-1.5,1.5)
    
    #Make the graph not looked squished - even out graph axis
    plt.gca().set_aspect('equal')
    
    return points
```

For `Generate_Polygon_Graph(3,0)`, we obtain:

<p align="center">
<img width="275" height="256" alt="Image" src="https://github.com/user-attachments/assets/1fa0325e-4c8a-416b-9fed-03d8f2b350f4" />
</p>

For `Generate_Polygon_Graph(4,0)`:

<p align="center">
<img width="275" height="256" alt="Image" src="https://github.com/user-attachments/assets/f8b806e0-5aee-4959-97ed-b89488a6eb86" />
</p>

And for `Generate_Polygon_Graph(5,0)`:

<p align="center">
<img width="275" height="256" alt="Image" src="https://github.com/user-attachments/assets/3e8130af-f55b-4f3f-83a7-24eec570dc4f" />
</p>

## Flatlands View

In this first model, “depth” is represented by the horizontal distance between the observer, which we will take to be the $x = 1$ line, and the visible boundary of the polygon at each vertical scanline. This distance is then visualised using a heatmap.

```python
def Flatlands_View(n,theta=0):
    """
    Generates and plots a front facing view of a n-sided polygon.
    
    n should be a positive integer.
    theta should be an angle between 0 and 360 degrees.
    """
    
    #Gather parameters
    tol = 1e-12
    p = Generate_Polygon(n)
    y_scan = np.linspace(-0.999,0.999,1999)
    
    #Adjust for angle
    theta = theta*np.pi/180
    
    transformation = np.array([[np.cos(theta), -np.sin(theta)],
                              [np.sin(theta), np.cos(theta)]])
    
    p = np.dot(p,transformation)
    
    scan_values = []

    for i in range(len(p)-1):
        for j in y_scan:
            if min(p[i][1], p[i+1][1]) - tol < j < max(p[i][1], p[i+1][1]) + tol:
                t = ((j - p[i][1])/(p[i+1][1] - p[i][1]))
                scan_values.append([(t*(p[i+1][0] - p[i][0]) + p[i][0]), round(j, 3)])
            else:
                continue

    scan_values = sorted(scan_values, key=lambda x: x[1])

    #Check visible lines. i.e for every unique y_scan value, find the max x.
    x_visible = []
    y_visible = []

    groups = defaultdict(list)

    for x,y in scan_values:
        groups[y].append(x)

    for y in sorted(groups.keys()):
        x_max = max(groups[y])
        x_visible.append(x_max)
        y_visible.append(y)
    
    #Fill empty areas with np.nan
    full_scan = defaultdict(lambda: np.nan)
    for x,y in zip(x_visible, y_visible):
        y_key = round(y,3)
        full_scan[y_key] = x
        
    x_scan = [full_scan[round(y,3)] for y in y_scan]
    
    #Create heatmap
    x = np.array(x_scan).reshape(1,len(x_scan))
    plt.imshow(x, cmap = 'plasma', vmax=1, vmin=-1, extent=[-1,1,-1,1])
    plt.gca().get_yaxis().set_visible(False)
    plt.colorbar()
    plt.gca().set_aspect(0.2)
    plt.show()
    
    return min(y_visible), max(y_visible), len(x_visible), len(y_visible), x_scan
```

For `Flatlands_View(3)`, we obtain:

<p align="center">
<img width="363" height="246" alt="Image" src="https://github.com/user-attachments/assets/bd6b87aa-23fa-481f-ba7c-9075ac899e0a" />
</p>

For `Flatlands_View(4)`:

<p align="center">
<img width="363" height="246" alt="Image" src="https://github.com/user-attachments/assets/63888075-1e1c-48e2-96c8-ff75a1cc3981" />
</p>

And for `Flatlands_View(5)`:

<p align="center">
<img width="363" height="246" alt="Image" src="https://github.com/user-attachments/assets/46ce7e8b-125c-4c3e-8b23-2aa4d551323c" />
</p>

## Rotation addition

You may ahve noticed that `Generate_Polygon_Graph` and `Flatlands_View` both take in an optional additional paremter `theta`. This parameter allows for rotational translation of the shape about the origin.

The rotation matrix in a 2-D plane is given as

| 1 | 2 | 3 |
|---|---|---|
| 4 | 5 | 6 |


## Future Extensions

The next steps are to include:

- Point perspective - Treating the observer, at least the view of the observer, as a point to provide a field of view like how 3D games work, rather than producing just a contour line of sorts.
- GIF/360 degree video of the polygon rotating.
