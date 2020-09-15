# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 13:05:20 2020

@author: kushaljadhav
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import random

#Configuration Space to display
ax = plt.gca()
obstacle = plt.Rectangle((5,3),width=3,height=3,facecolor="yellow",edgecolor="black")
ax.add_patch(obstacle)
initial = plt.scatter(1,10,100)
end = plt.scatter(10,0,100)
#Initialize the parameters
start=[1,10]    #Initialize start node
goal=[10,0]     #Initialize goal node
obstacles=[]    #List of all the obstacles
possiblenodes=[]    #All the possible nodes to expand
rnd=[]       #List of random nodes
max_iteration=500      #Number of maximum iterations
for i in range(5,8):    
    for j in range(3,6):
        obstacles.append([i,j])         #Complete the list of obstacles
        
def euler(node,theta,dt):   #Euler's integration to traverse the path in time intervals dt
     
    rturn=2
    theta1=theta+(dt/rturn)         #rturn is the turning radius
    
    node[0]=node[0]+node[0]*math.cos(theta1)*dt  #Velocity is considered to be 1 so not mentioned in the equations
    node[1]=node[1]+node[1]*math.sin(theta1)*dt
    
    return node[0],node[1]        
        
        
def expand(x_nearest,x_rand,theta,time_window,dt,obs):
    
    intsteps=int(math.floor(time_window/dt))        #Number of steps to perform integration
    for j in range(intsteps):
        x_prev=x_nearest
        x_new = euler(x_prev,theta,dt) 
        if x_new in obs:
            print("collision")
            continue
        else :
            dist = math.sqrt((x_new[0]-x_rand[0])**2 + (x_new[1]-x_rand[1])**2) #To calculate distance between expanded node and random node
        return x_new,dist
   
exp_nodes = []   
dista = []
nearby=[]     

for k in range(max_iteration):       #Maximum Iterations        
    rnd=[int(random.uniform(1,20)),int(random.uniform(1,20))]  #Generate a random node
    
    possiblenodes=[start]       #First element of the list of possible nodes is start    
    if rnd in obstacles:    #If random node is in obstacle leave the if loop and continue the for loop
        print("collision")
        continue
    else:
        dist = []   #List of distances of the random node to the possible node
        for i in possiblenodes:
            dist.append(int(math.sqrt(((i[0]-rnd[0])**2)+((i[1]-rnd[1])**2))))   
        index=dist.index(min(dist))         #Find the minimum distance and the index of that nearby node
        nearby=possiblenodes[index]         #Select nearby node from the list of possible nodes
        #Function to steer car left for window time of 2 secs and delta time as 0.2 
        exp1,dist1=expand(nearby,rnd,-np.pi/4,3,0.2,obstacles)
        #If we change the values of dt,window size and theta than we will get closer to the goal node.
        exp_nodes.append(exp1)
        dista.append(dist1)#Distance Travelled from expanded node to random node
        #Function to steer car left for window time of 2 secs and delta time as 0.2 
        exp2,dist2=expand(nearby,rnd,0,3,0.2,obstacles)
        exp_nodes.append(exp2)
        dista.append(dist2)#Distance travelled from expanded node to random node
        #Function to steer car right for window time of 2 secs and delta time as 0.2 
        exp3,dist3=expand(nearby,rnd,np.pi/4,3,0.2,obstacles)
        exp_nodes.append(exp3)
        dista.append(dist3)   #Distance travelled from expanded node to random node
        
        req_index = dista.index(min(dista))     #Minimum distance from all the 3 expanded nodes
        expanded_node = exp_nodes[req_index]    #Choose the node with the minimum distance as expanded node
             
           
                               
    #distance between expanded node and random node
        dist_exp_rnd = int(math.sqrt(((expanded_node[0]-rnd[0])**2)+((expanded_node[1]-rnd[1])**2)))
        
    #distance from random node to goal node
        dist_rand_fin = int(math.sqrt(((rnd[0]-goal[0])**2)+((rnd[1]-goal[1])**2)))
        
    
        if dist_exp_rnd < dist_rand_fin:
          print("Reached goal")
          plt.scatter(expanded_node[0],expanded_node[1],50) #Plot the expanded nodes
          break
            
    
 




        
    

