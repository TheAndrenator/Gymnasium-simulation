# ## ANDRES GRACIA GUILLEN
# ## A* ALGORITHM

#! /usr/bin/env python

"""
# Notation

## Map

In the original map:

* 0: free
* 1: occupied (wall/obstacle)

Via code, we incorporate:

* 2: visited
* 3: start
* 4: goal
* 5: path

## Node

# Specific to Python implementation

* Indices start at 0
* charMap
"""

"""
# Coordinate Systems for `.csv` and `print(numpy)`

X points down (rows); Y points right (columns); Z would point outwards.

*--> Y (columns)
|
v
X (rows)
"""

import heapq

import termios
import tty
import sys
import gymnasium as gym
import gymnasium_csv
from gymnasium_csv.wrappers import BoxToDiscreteObservation

import numpy as np
import time

# # Movement assignations
UP = 0
UP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN = 4
DOWN_LEFT = 5
LEFT = 6
UP_LEFT = 7

SIM_PERIOD_MS = 500.0

# # Initial values are hard-coded (At map level)
FILE_NAME = '../assets/map1.csv'
START_X = 1
START_Y = 1
END_X = 10
END_Y = 10

# Environment setup
env = gym.make('gymnasium_csv-v0',
               render_mode='human',  # "human", "text", None
               inFileStr='../assets/map1.csv',
               initX=1,
               initY=1,
               goalX=10,
               goalY=10) 
observation, info = env.reset() # Reset the environment
print("observation: "+str(observation)+", info: "+str(info))
env.render() # Render the environment
time.sleep(0.5)

# # Define class for nodes (at the graph/node level)
class Node:
    def __init__(self, x, y, g):
        self.x = x
        self.y = y
        self.g = g

    def __lt__(self, other):
        return self.g < other.g

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | g_value "+str(self.g))
        
# # Define function to calculate heuristic (Manhattan distance)
def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

# Implement algorithm A* given a map, an initial node and a target node.
def a_star_search(charMap, init, goal):
    open_list = [(init.g + heuristic(init, goal), init)]  # Node priority queue
    closed_list = {}  # Store the previous node in the optimal path
    g_list = {}  # Stores the g values for nodes
    reward = 0

    g_list[(init.x, init.y)] = 0

    while open_list:  # Main loop (as long as the priority queue is not empty)
        _, current = heapq.heappop(open_list)  # Extract the node with the lowest total cost (f_cost)

        if current.x == goal.x and current.y == goal.y:  # If the current node is the target
            # Reconstructing the optimal path
            path = [current]
            while (current.x, current.y) in closed_list:
                current = closed_list[(current.x, current.y)]
                path.append(current)
            return list(reversed(path))

        # Analyze adjacent nodes (right, left, bottom, top)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            tmpX = current.x + dx
            tmpY = current.y + dy

            # Check that the adjacent node is valid (not outside the map or an obstacle).
            if 0 <= tmpX < len(charMap) and 0 <= tmpY < len(charMap[0]) and charMap[tmpX][tmpY] != '1':
                
                newNode = Node(tmpX, tmpY, g_list[(current.x, current.y)] + 1)

                # Check that the adjacent node has not been visited or that the new path is a better one
                if (newNode.x, newNode.y) not in g_list or g_list[(newNode.x, newNode.y)] > newNode.g:
                    g_list[(newNode.x, newNode.y)] = newNode.g  # Store new g score
                    f_cost = newNode.g + heuristic(newNode, goal)  # Calculate total node cost

                    closed_list[(newNode.x, newNode.y)] = current  # Store the previous node in the optimal path
                    heapq.heappush(open_list, (f_cost, newNode))  # Add node to priority queue

                    ## Movements for Gymnasium simulation environment

                    if reward != 1:  # If the target has not been reached
                        if dx == 0 and dy == 1:
                            # Move right
                            observation, reward, terminated, truncated, info = env.step(RIGHT)
                            env.render() # Render the environment
                            print("RIGHT | observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
                                str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
                            time.sleep(SIM_PERIOD_MS/1000.0) # Sleep for simulation period
                        elif dx == 0 and dy == -1:
                            # Move left
                            observation, reward, terminated, truncated, info = env.step(LEFT)
                            env.render()
                            print("LEFT | observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
                                str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
                            time.sleep(SIM_PERIOD_MS/1000.0)
                        elif dx == 1 and dy == 0:
                            # Move down
                            observation, reward, terminated, truncated, info = env.step(DOWN)
                            env.render()
                            print("DOWN | observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
                                str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
                            time.sleep(SIM_PERIOD_MS/1000.0)
                        elif dx == -1 and dy == 0:
                            # Move up
                            observation, reward, terminated, truncated, info = env.step(UP)
                            env.render()
                            print("UP | observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
                                str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
                            time.sleep(SIM_PERIOD_MS/1000.0)
                        
                        if reward == 1:
                            # Target reached
                            print("\n\n--- Target reached! ---\n\n")
                            time.sleep(2)
                            break

                    # Mark node as visited (except for initial and target nodes)
                    if charMap[newNode.x][newNode.y] != '3' and charMap[newNode.x][newNode.y] != '4':
                        charMap[newNode.x][newNode.y] = '2'

    return None  # if a path was not found

# # Map

# ## Create data structure for map

charMap = []

# ## Create function to dump data structure for map

def dumpMap():
    for line in charMap:
        print(line)

# ## From file, fill file data structure (`to parse`/`parsing`) to map

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

# ## At the map level, we integrate the info we had from start & end

charMap[START_X][START_Y] = '3' # 3: initial node
charMap[END_X][END_Y] = '4' # 4: target node

# ## Dump map by console

print("\nOriginal map:")
dumpMap()

# ## Definition of initial and target nodes

init = Node(START_X, START_Y, 0)
goal = Node(END_X, END_Y, 0)

# ## Execute algorithm A*

path = a_star_search(charMap, init, goal)

# ## Mark path on map and print list of path nodes

print("\nPath nodes:")
if path:
    for node in path:
        x, y = node.x, node.y
        if charMap[x][y] != '3' and charMap[x][y] != '4':
            charMap[x][y] = '5' # 5: path
            node.dump()

print("\nMap with path:")
dumpMap()
env.render()
