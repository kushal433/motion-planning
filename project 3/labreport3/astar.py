# astar.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Clemson University and the authors.
# 
# Author: Ioannis Karamouzas (ioannis@g.clemson.edu)
#


# Compute the optimal path from start to goal.
# The car is moving on a 2D grid and
# its orientation can be chosen from four different directions:
forward = [[-1,  0], # 0: go north
           [ 0, -1], # 1: go west
           [ 1,  0], # 2: go south
           [ 0,  1]] # 3: go east

# The car can perform 3 actions: -1: right turn and then move forward, 0: move forward, 1: left turn and then move forward
action = [-1, 0, 1]
action_name = ['R', 'F', 'L']
cost = [1, 1, 1] # corresponding cost values

# GRID:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = (4, 3, 0) # (grid row, grid col, orientation)
                
goal = (2, 0, 1) # (grid row, grid col, orientation)


heuristic = [[2, 3, 4, 5, 6, 7], # Manhattan distance
        [1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7]]

from utils import (Value, OrderedSet, PriorityQueue)

"""
Two data structures are provided for your open and closed lists: 

 1. OrderedSet is an ordered collection of unique elements.
 2. PriorityQueue is a key-value container whose `pop()` method always pops out
    the element whose value has the highest priority.

 Common operations of OrderedSet, and PriorityQueue
   len(s): number of elements in the container s
   x in s: test x for membership in s
   x not in s: text x for non-membership in s
   s.clear(): clear s
   s.remove(x): remove the element x from the set s;
                nothing will be done if x is not in s

 Unique operations of OrderedSet:
   s.add(x): add the element x into the set s
   s.pop(): return and remove the LAST added element in s;

 Example:
   s = Set()
   s.add((0,1,2))    # add a triplet into the set
   s.remove((0,1,2)) # remove the element (0,1,2) from the set
   x = s.pop()

 Unique operations of PriorityQueue:
   PriorityQueue(order="min", f=lambda v: v): build up a priority queue
       using the function f to compute the priority based on the value
       of an element
   s.put(x, v): add the element x with value v into the queue
                update the value of x if x is already in the queue
   s.get(x): get the value of the element x
            raise KeyError if x is not in s
   s.pop(): return and remove the element with highest priority in s;
            raise IndexError if s is empty
            if order is "min", the element with minimum f(v) will be popped;
            if order is "max", the element with maximum f(v) will be popped.
 Example:
   s = PriorityQueue(order="min", f=lambda v: v.f)
   s.put((1,1,1), Value(f=2,g=1))
   s.put((2,2,2), Value(f=5,g=2))
   x, v = s.pop()  # the element with minimum value of v.f will be popped
"""

# ----------------------------------------
# modify the code below
# ----------------------------------------

#Function to find the cost of neighbors 
def costfunction(node,neighbor):
    if(node[2] == 0 and neighbor[2] == 0):  #facing North
        return cost[1]
    elif (node[2] == 0 and neighbor[2] == 1):
        return cost[2]
    elif (node[2] == 0 and neighbor[2] == 3):
        return cost[0]
    elif (node[2] == 1 and neighbor[2] == 1):  #facing West
        return cost[1]
    elif (node[2] == 1 and neighbor[2] == 2):
        return cost[2]
    elif (node[2] == 1 and neighbor[2] == 0):
        return cost[0]
    elif (node[2] == 2 and neighbor[2] == 2): #facing South
        return cost[1]
    elif (node[2] == 2 and neighbor[2] == 1):
        return cost[0]
    elif (node[2] == 2 and neighbor[2] == 3):
        return cost[2]
    elif (node[2] == 3 and neighbor[2] == 0):   #facing East
        return cost[2]
    elif (node[2] == 3 and neighbor[2] == 3):
        return cost[1]
    elif (node[2] == 3 and neighbor[2] == 2):
        return cost[0]
     
   #function to get the neighbors 
def get_neighbors(current):
    neighbors = []

#facing North 
    temp = list(current)
    current = list(current)
    if temp[2] == 0:#facing North
        temp[0] = current[0] - 1
        neighbors.append(tuple(temp))
        temp[1] = current[1] - 1
        neighbors.append(tuple(temp))
        temp[1] = current[1] + 1
        neighbors.append(tuple(temp))
    elif temp[2] == 1:    #facing West
        temp[1] = current[1] - 1
        neighbors.append(tuple(temp))
        temp[0] = current[0] - 1
        neighbors.append(tuple(temp))
        temp[0] = current[0] + 1
        neighbors.append(tuple(temp))
    elif temp[2] == 2: #facing South
        temp[0] = current[0] + 1
        neighbors.append(tuple(temp))
        temp[1] = currrent[1] - 1
        neighbors.append(tuple(temp))
        temp[1] = current[1] + 1
        neighbors.append(tuple(temp))
    elif temp[2] == 3:         #facing East
        temp[0] = current[0] - 1
        neighbors.append(tuple(temp))
        temp[0] = current[0] + 1
        neighbors.append(tuple(temp))
        temp[1] = current[1] + 1
        neighbors.append(tuple(temp))
    
    #to discard the unnavigable space from the neighbors list
    for i in range(0,5):
        for j in range(0,6):
            if grid[i][j] == 1:
                for x in neighbors:
                    if x[0] == i and x[1] == j:
                        neighbors.remove(x)

    return neighbors



def compute_path(grid,start,goal,cost,heuristic):
   
    # Use the OrderedSet for your closed list
    closed_set = OrderedSet()
    
    # Use thePriorityQueue for the open list
    open_set = PriorityQueue(order=min, f=lambda v: v.f)      

    # Keep track of the parent of each node. Since the car can take 4 distinct orientations, 
    # for each orientation we can store a 2D array indicating the grid cells. 
    # E.g. parent[0][2][3] will denote the parent when the car is at (2,3) facing up    
    parent = [[[' ' for row in range(len(grid[0]))] for col in range(len(grid))], 
             [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
             [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
             [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]]

    # The path of the car
    path =[['-' for row in range(len(grid[0]))] for col in range(len(grid))]
    
    x = start[0] 		
    y = start[1]
    theta = start[2]   
    h = heuristic[x][y]
    g = 0
    f = g+h
    open_set.put(start, Value(f=f,g=g))

    # your code: implement A*
    # Initially you may want to ignore theta, that is, plan in 2D.
    # To do so, set actions=forward, cost = [1, 1, 1, 1], and action_name = ['U', 'L', 'R', 'D']
    # Similarly, set parent=[[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    while open_set:
        node = open_set.pop()
        closed_set.add(node[0])
        if node[0] == goal:
            break
      
#finding child of node
#write function for finding child node
#setting the cost values for neighboring nodes
        neighbors = get_neighbors(node[0])
        print(neighbors)
        for i in neighbors:
            x = i[0] 
            y = i[1]
            theta = i[2]
            h = heuristic[x][y]
            g = node[1].g + costfunction(node[0],i)
            f = g+h
            if i not in open_set or i not in closed_set:
                open_set.put(i,Value(f,g))
            elif i in open_set and f < open_set.get(i).f:
                open_set.put(i,Value(f,g))
                
        
        return path, closed_set


if __name__ == "__main__":
    path,closed=compute_path(grid, init, goal, cost, heuristic)

    for i in range(len(path)):
        print(path[i])

    print("\nExpanded Nodes")    
    for node in closed:
        print(node)

"""
To test the correctness of your A* implementation, when using cost = [1, 1, 10] your code should return 

['-', '-', '-', 'R', 'F', 'R']
['-', '-', '-', 'F', '-', 'F']
['*', 'F', 'F', 'F', 'F', 'R']
['-', '-', '-', 'F', '-', '-']
['-', '-', '-', 'F', '-', '-'] 

In this case, the elements in your closed set (i.e. the expanded nodes) are: 
(4, 3, 0)
(3, 3, 0)
(2, 3, 0)
(2, 4, 3)
(1, 3, 0)
(2, 5, 3)
(0, 3, 0)
(0, 4, 3)
(0, 5, 3)
(1, 5, 2)
(2, 5, 2)
(2, 4, 1)
(2, 3, 1)
(2, 2, 1)
(2, 1, 1)
(2, 0, 1)

"""