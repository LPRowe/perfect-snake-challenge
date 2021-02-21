# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:04:56 2021

@author: rowe1
"""

def a_star(start, target, tail, grid, graph, obstacles):
    """
    Uses a_star heuristic to find a path from start to target and back to tail.
    If such a path exists, return the path from start to target.
    
    If such a path does not exist, returns a path from start to tail.
    
    Cannot revisit the same node twice and cannot step on obstacles if obstacles[node] < k
    where k is the number of steps taken so far.
    
    Having a hashmap of obstacles allows for O(1) lookup times to see if a node is taken and
    allows us to account for the snake's tail moving as we take steps forward without actually
    updating the datastucture.
    """
    