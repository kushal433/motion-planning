# simulator.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Clemson University and the author.
# 
# Author: Ioannis Karamouzas (ioannis@g.clemson.edu)
#

import numpy as np
from math import sqrt

class Agent(object):

    def __init__(self, csvParameters, ksi=0.5, dhor = 10, timehor=5, goalRadiusSq=1, maxF = 10):
        """ 
            Takes an input line from the csv file,  
            and initializes the agent
        """
        self.id = int(csvParameters[0]) # the id of the agent
        self.gid = int(csvParameters[1]) # the group id of the agent
        self.pos = np.array([float(csvParameters[2]), float(csvParameters[3])]) # the position of the agent 
        self.vel = np.zeros(2) # the velocity of the agent
        self.goal = np.array([float(csvParameters[4]), float(csvParameters[5])]) # the goal of the agent
        self.prefspeed = float(csvParameters[6]) # the preferred speed of the agent
        self.gvel = self.goal-self.pos # the goal velocity of the agent
        self.gvel = self.gvel/(sqrt(self.gvel.dot(self.gvel )))*self.prefspeed       
        self.maxspeed = float(csvParameters[7]) # the maximum sped of the agent
        self.radius = float(csvParameters[8]) # the radius of the agent
        self.goalRadiusSq = goalRadiusSq # parameter to determine if agent is close to the goal
        self.atGoal = False # has the agent reached its goal?
        self.ksi = ksi # the relaxation time used to compute the goal force
        self.dhor = dhor # the sensing radius
        self.timehor = timehor # the time horizon for computing avoidance forces
        self.F = np.zeros(2) # the total force acting on the agent
        self.maxF = maxF # the maximum force that can be applied to the agent

    def computeForces(self, neighbors=[]):
         
         cost_old = float('inf')
        zeta=0.5
        
        nearby=[]
        curr_vel = self.gvel[:]
        #To determine the neighbors
        for i in neighbors:
            if self.id != i.id:
                if sqrt((self.pos[0]-i.pos[0])**2+(self.pos[1]-i.pos[1])**2)<self.dhor:
                    nearby.append(i)
                
        def ttc(i,j,vcan):
            rad=i.radius+j.radius
            
            w = [i.pos[0] - j.pos[0],i.pos[1] - j.pos[1]]
            c = np.dot(w,w)-np.dot(rad,rad)
           

            if c<0:
                return 0
            v = [vc[0] - j.vel[0],vc[1] - j.vel[1]]
            
            a=np.dot(v,v)
            b = np.dot(w,v)
            
            if b>0:
                print("Collision")
                return float('inf')
            
            discr=b*b-a*c
            
            if discr<=0:
                return float('inf')
            
            tau=(c/(-b+sqrt(discr)))      #smallest root
            print(tau)
            if tau<0:
                return float('inf')
            return tau,v
              
#uniformly sampling 200 velocities and determining candidate velocity
        vc = []
        
        
        for i in range(0,200):
            length = self.maxspeed*np.sqrt(np.random.uniform(0, 1))
            #length=np.random.uniform(0,1)
            angle=  np.pi * np.random.uniform(0, 2)
            vc = [length * np.cos(angle),length * np.sin(angle)]

           
    #to find time to collision ttc
            mt = float('inf')
            for j in nearby:
                tc =  ttc(self,j,vc)
                if tc > 0 and tc < mt:
                    mt = tc
    

            """
            Your code to compute the forces acting on the agent. 
            You probably need to pass here a list of all the agents in the simulation to determine the agent's nearest neighbors
        """       
        if not self.atGoal:
            self.F = np.zeros(2)
        
        Fg=(gvel-v)/zeta 
        print(Fg) 
            

    def update(self, dt):
        """ 
            Code to update the velocity and position of the agents.  
            as well as determine the new goal velocity 
        """
        if not self.atGoal:
            self.vel += self.F*dt     # update the velocity
            self.pos += self.vel*dt   #update the position
        
            # compute the goal velocity for the next time step. Do not modify this
            self.gvel = self.goal - self.pos
            distGoalSq = self.gvel.dot(self.gvel)
            if distGoalSq < self.goalRadiusSq: 
                self.atGoal = True  # goal has been reached
            else: 
                self.gvel = self.gvel/sqrt(distGoalSq)*self.prefspeed  
            
            
  