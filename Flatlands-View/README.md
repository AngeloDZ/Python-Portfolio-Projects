# Flatlands View

## Overview

This project was inspired by [*Flatland: A Romance of Many Dimensions*](https://en.wikipedia.org/wiki/Flatland), a novella written by Edwin Abbott Abbott.

The book entails the story of a square who lives in a world called Flatland. Flatland is inhabited by 2-dimensional polygons, dubbed flatlanders.

As they are two dimensional, the flatlanders are only able to visually see one another as one dimensional line segments. However, they are able to identify one another through depth perception, allowing them to identify how many sides each person has.

This book inspired me to create a function in python that would create a visualisation to replicate how an inhabitant of Flatland would view other flatlanders. 

## Contents

## Idea

The idea I came up with was for our regular polygon to have a center at (0,0), whilst having a circumcircle with radius 1 unit. Then the $x = 1$ line could act as the 'observer'.

The plan was to then visualise what the $x = 1$ line 'saw' by seeing how far the shape was from the $x = 1$ line for every y value. In this case $y ∈ [-1,1]$. Then, we can calculate the distance from each coordinate on the visible side of the polygon, and translate it into some sort of heatmap that acts almost like contour lines, giving the perception of depth.

## Generate Polygon

For the first part of the visualisation, I would first have to create a function which constructs a regular n-sided polygon.

We can use the fact that for regular polygons, the angle ath the centre between two adjacent corners will be equal to $360°/n$, thus, given one coordinate of the polygon, we can calculate the coordinates of the rest of the corners using trigonometry.
