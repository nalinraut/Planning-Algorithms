#@Nalin Raut

import gym
import random
import os
import numpy as np
import rrt_fetch

##############################################################################################################################

# RRT 

print("Enter 1 for the Smoothened Path.\nEnter 2 for the Actual Path.")
i = int(input("\nEnter your Response: "))
print('\n=====================================================================\n')

fetch_path, extend_path = rrt_fetch.main()
start = [-100,-100,-100, 1]

for fp in fetch_path:
	fp.append(0)

for ex in extend_path:
	ex.append(0)

extend_path = np.array([start] + extend_path[::-1])
extend_path = np.divide(extend_path[:], 10)

fetch_path = np.array([start] + fetch_path[::-1])
fetch_path = np.divide(fetch_path[:], 10)

#############################################################################################################################

# SIMULATION


env = gym.make('FetchReach-v1')
env.reset()
env.render()
print('\n=====================================================================\n')

if i == 1:
	action = fetch_path #Connect Path
	print("\nSimulation Initiated.\n")
	time_step = 20

elif i == 2:
	action = extend_path # Extend Path
	print("Simulation Initiated.\n")
	print("\nSimulating Actual Path takes time")
	time_step = 20

for i in range (len(action)):
	act = np.array(action[i])
	print("Currently at Position: ",act)

	for _ in range(time_step):
		env.step(act)
		env.render()
print("End of Simulation")



#############################################################################################################################

# TOTAL COST FOR THE PATH

total_connect = 0
for i in range(len(fetch_path)):
	con=0
	for j in range(3):
		con = con + np.square(fetch_path[i][j])
	total_connect = total_connect + np.sqrt(con)


total_extend = 0
for i in range(len(extend_path)):
	ext=0
	for j in range(3):
		ext = ext + np.square(extend_path[i][j])
	total_extend = total_extend + np.sqrt(ext)

print('\n======================================================================\n')
print("Total cost of the smoothened path: ", (total_connect))
print("Total cost of the actual path: ", (total_extend))
	
#############################################################################################################################