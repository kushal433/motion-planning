Members of group:
1. Kushal Jadhav
2. Siddish Prabhakara Rao

We have performed the simulation for various values of alpha, beta and gamma in the cost function.
These are some of the values we tried:
3 agents:
	alpha   beta     gamma
	1        1        2
	1	 2	  3
	1	 0.5  	  2
	2	 1	  3
	3	 2	  1
	1	 1 	  3



8 agents:
	alpha   beta    gamma
	1        1	 2
	1	 2	 3
	1	 0.5	 2
	1	 1	 1
	2	 1	 1
	1	 1	 3


We found alpha = 1,beta = 1,gamma = 3 to be working successfully for both simulations. 
The simulations for both 3 and 8 agents have been exported to a csv file by setting
the doExport flag to True. The sensing radius we used was 8 and we ran it for 200 candidate velocities.
	