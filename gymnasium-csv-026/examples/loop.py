# ## ANDRES GRACIA GUILLEN
# ## SEQUENCE SEARCH

#!/usr/bin/env python

import gymnasium as gym
import gymnasium_csv

import numpy as np
import time

"""
# Coordinate Systems for `.csv` and `print(numpy)`

X points down (rows); Y points right (columns); Z would point outwards.

*--> Y (columns)
|
v
X (rows)
"""

# Movement assignations
UP = 0
UP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN = 4
DOWN_LEFT = 5
LEFT = 6
UP_LEFT = 7

SIM_PERIOD_MS = 500.0

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

# Movement sequence to reach the target

for i in range(7):
    # Move right 7 positions
    observation, reward, terminated, truncated, info = env.step(RIGHT)
    env.render() # Simulate the movement
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0) # Wait for the simulation to finish

for i in range(2):
    # Move diagonal down-right 2 positions
    observation, reward, terminated, truncated, info = env.step(DOWN_RIGHT)
    env.render()
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0)

for i in range(2):
    # Move diagonal down-left 2 positions
    observation, reward, terminated, truncated, info = env.step(DOWN_LEFT)
    env.render()
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0)

for i in range(2):
    # Move left 2 positions
    observation, reward, terminated, truncated, info = env.step(LEFT)
    env.render()
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0)

for i in range(3):
    # Move diagonal down-left 3 positions
    observation, reward, terminated, truncated, info = env.step(DOWN_LEFT)
    env.render()
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0)

for i in range(1):
    # Move diagonal down-right 1 position
    observation, reward, terminated, truncated, info = env.step(DOWN_RIGHT)
    env.render()
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0)

for i in range(5):
    # Move right 5 positions
    observation, reward, terminated, truncated, info = env.step(RIGHT)
    env.render()
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0)

for i in range(1):
    # Move diagonal down-right 1 position
    observation, reward, terminated, truncated, info = env.step(DOWN_RIGHT)
    env.render()
    print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
          str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
    time.sleep(SIM_PERIOD_MS/1000.0)

if reward == 1:
    # Target reached
    print("\n\n--- Target reached! ---\n\n")
    time.sleep(2)
