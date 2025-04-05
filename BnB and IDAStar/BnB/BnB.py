"""
Assignment 2: Search and Optimization

Team Members
CS24M101 - A Sai Jagadeesh
CS24M111 - G Kavyasri

-------------------------------------
Frozen Lake using Branch and Bound
-------------------------------------
"""

import imageio
import matplotlib.pyplot as plt
import gymnasium as gym
import numpy as np
import time

def branchAndBoundDFS(environment, currState, pathSoFar, visited, cost, goalState, bestPath, minimumCost, explored):
    if currState in visited and visited[currState] <= cost:
        return

    visited[currState] = cost
    pathSoFar.append(currState)
    explored.append(currState)

    if currState == goalState:
        if cost < minimumCost[0]:
            minimumCost[0] = cost
            bestPath.clear()
            bestPath.extend(pathSoFar)
        return

    for action in range(environment.action_space.n):
        for _, nextState, _, done in environment.unwrapped.P[currState][action]:
            if done and nextState != goalState:
                continue
            branchAndBoundDFS(environment, nextState, pathSoFar[:], visited.copy(), cost + 1, goalState, bestPath, minimumCost, explored)

def solveFrozenLakeBnB(environment):
    currState, _ = environment.reset()
    goalState = environment.observation_space.n - 1
    minimumCost = [float('inf')]
    bestPath = []
    explored = []

    branchAndBoundDFS(environment, currState, [], {}, 0, goalState, bestPath, minimumCost, explored)

    return bestPath, explored

def getTimeOfBnB(algorithm, environment):
    startTime = time.time()
    bestPath, exploredPath = algorithm(environment)
    print(bestPath)
    print(exploredPath)
    elapsedTime = time.time() - startTime

    if elapsedTime > 600:
        return [], [], 600

    return bestPath, exploredPath, elapsedTime

def generateGIF(environment, finalPath, exploredPath, filename):
    frames = []
    environment.reset()

    for currState in exploredPath:
        environment.unwrapped.s = currState
        frame = environment.render()
        frames.append(frame)
        if currState == finalPath[-1]:
            break

    frames += [frames[-1]] * 5
    for currState in finalPath:
        environment.unwrapped.s = currState
        frame = environment.render()
        frames.append(frame)

    imageio.mimsave(filename, frames, duration=0.3, loop=0)
    print("Saved animated GIF: ", filename)


environment = gym.make("FrozenLake-v1", is_slippery=False, render_mode="rgb_array")

timeTaken = []

for i in range(5):
    print("Run ", i+1, "/5 - Branch and Bound")
    finalPath, exploredPath, timeOfBnB = getTimeOfBnB(solveFrozenLakeBnB, environment)
    if finalPath:
        generateGIF(environment, finalPath, exploredPath, f"bnb_run_{i+1}.gif")
        timeTaken.append(timeOfBnB)

plt.plot(range(1, len(timeTaken) + 1), timeTaken, marker='x', linestyle=':', color='crimson', label="Branch and Bound")
plt.xlabel("Run")
plt.ylabel("Time in seconds")
plt.title("Performance of Branch and Bound on Frozen Lake")
plt.legend()
plt.grid()
plt.savefig("BnB_plot.png")
print("Saved plot: BnB_plot.png")
