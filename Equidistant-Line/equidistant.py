# -*- coding: utf-8 -*-
"""
Created on Tue May 13 08:53:05 2025

@author: julia
"""
import numpy as np
import matplotlib.pyplot as plt

def Equidistant_line(a,b):
    """
    Returns the type of slope, the slope coefficient and the midpoint between two points a and b. Plots the equidistant line.
    Each point should be a tuple like (x1, y1).
    """
    plt.scatter(a[0],a[1])
    plt.scatter(b[0],b[1])
    
    centre = (((a[0] + b[0])/2),((a[1]+b[1])/2))
    plt.scatter(centre[0],centre[1])
    
    x = np.linspace(min(a[0],b[0]),max(a[0],b[0]),100)
    
    # Both x and y coordinates are different
    if a[0] == b[0] and a[1] == b[1]:
        
        print("Cannot use the same point twice!")
        
        return None
        
    # x-coordinates are the same
    elif a[0] == b[0]:
        
        plt.axhline(centre[1])
        
        return {"type": "horizontal",
                "slope": "0",
                "midpoint": centre}
    
    # y-coordinates are the same
    elif a[1] == b[1]:
        
        plt.axvline(centre[0])
        
        return {"type": "vertical",
                "slope": "inf",
                "midpoint": centre}
    
    # Both x and y coordinates are different
    else:
        slope_coefficient = (a[1]-b[1])/(a[0]-b[0])
        
        perpendicular_slope_coefficient = -1/slope_coefficient
        
        c = centre[1] - perpendicular_slope_coefficient * centre[0]
        
        y = perpendicular_slope_coefficient * x + c
        
        plt.plot(x,y)
    
        return {"type": "diagonal",
                "slope": perpendicular_slope_coefficient,
                "midpoint": centre}
        
    
        
        