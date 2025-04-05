"""
Assignment 2: Search and Optimization

Team Members
CS24M101 - A Sai Jagadeesh
CS24M111 - G Kavyasri
-------------------------------------
Frozen Lake using IDA*
-------------------------------------
"""

import imageio
import matplotlib.pyplot as plt
import gymnasium as gym
import numpy as np
import time


def heuristicManhattanDis(currState, goalState, ncol):
    currStateRow = currState//ncol
    currStateCol = currState % ncol
    goalStateRow = goalState//ncol
    goalStateCol = goalState % ncol
    return abs(currStateRow - goalStateRow) + abs(currStateCol - goalStateCol)

def idaStarDFS(environment, currState, pathSoFar, GCost, upperBound, goalState, bestPath, minimumCost, explored):
    h = heuristicManhattanDis(currState, goalState, environment.unwrapped.ncol)
    f = GCost + h

    if f > upperBound:
        return f

    explored.append(currState)

    if (currState == goalState):
        if (GCost < minimumCost[0]):
            minimumCost[0] = GCost
            bestPath.clear()
            bestPath.extend(pathSoFar)
        return -1

    newUpperBound = float('inf')

    for action in range(environment.action_space.n):
        for _, nextState, _, _ in environment.unwrapped.P[currState][action]:
            if nextState in pathSoFar:
                continue
            pathSoFar.append(nextState)
            result = idaStarDFS(environment, nextState, pathSoFar, GCost + 1, upperBound, goalState, bestPath, minimumCost, explored)
            newUpperBound = min(newUpperBound, result)
            pathSoFar.pop()

            if result == -1:
                return -1

    return newUpperBound

def solveFrozenLake(environment):
    currState , info = environment.reset()
    goalState = environment.observation_space.n - 1
    upperBound = heuristicManhattanDis(currState, goalState, environment.unwrapped.ncol)

    bestPath = []
    minimumCost = [float('inf')]
    explored = []

    while True:
        result = idaStarDFS(environment, currState, [currState], 0, upperBound, goalState, bestPath, minimumCost, explored)
        if result == -1:
            break
        if result == float('inf'):
            return [], []
        upperBound = result

    return bestPath, explored

def getTimeOfIDA(algorithm, environment):
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
    
    for currState in finalPath:
        environment.unwrapped.s = currState
        frame = environment.render()
        frames.append(frame)

    imageio.mimsave(filename, frames, duration=0.3, loop=0)
    print("Saved animated GIF: ", filename)


environment = gym.make("FrozenLake-v1", is_slippery=False, render_mode="rgb_array")

timeTaken = []

for i in range(5):
    print("Run ", i+1, "/5 - IDA*")
    finalPath, exploredPath, timeofIDA = getTimeOfIDA(solveFrozenLake, environment)
    if finalPath:
        generateGIF(environment, finalPath, exploredPath, f"ida_run_{i+1}.gif")
        timeTaken.append(timeofIDA)
 
plt.plot(range(1, len(timeTaken) + 1), timeTaken, marker='s', linestyle='--', label="IDA*")
plt.xlabel("Run")
plt.ylabel("Time in seconds")
plt.title("Performance of IDA* on Frozen Lake")
plt.legend()
plt.grid()
plt.savefig("IDAStar_plot.png")
