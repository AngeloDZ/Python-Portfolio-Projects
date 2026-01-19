# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def Generate_Polygon_Graph(n,theta):
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

def Flatlands_View(n, theta):
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
    
    #Fill empty areas with 
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

#Add more comments
