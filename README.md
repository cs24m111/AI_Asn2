# AI_Asn2
AI_ Assignment2

# AI Assignment 2: Search and Optimization

## Overview

Implement all the mentioned algorithms on one of the given environments and record the performance (reward, time, point of convergence). You are expected to submit a replicable GitHub repository and present a slide deck (maximum of six slides) on the results, explaining the reasons behind the observed performances. The slide deck should include GIFs of the implemented algorithms being executed in the environment, and you should also mention the heuristic function used.

## Algorithms to Implement
- **Branch and Bound**
- **Iterative Deepening A***
- **Hill Climbing**
- **Simulated Annealing**

## Environments
- **For Branch and Bound & Iterative Deepening A*:**
  - Frozen Lake
  - Ant Maze
- **For Hill Climbing & Simulated Annealing:**
  - Traveling Salesman Problem

## Experimentation Details

### For Branch and Bound & Iterative Deepening A*
- **Objective:** Plot the average time taken to reach the goal state.
- **Testing:** Run at least five experiments.
- **Termination:** Terminate the run if the goal state isn't reached even after some time τ has passed (consider τ = 10 minutes; modify as required).

### For Hill Climbing & Simulated Annealing
- **Objective:** Plot the average time taken to reach an optimum.
- **Testing:** Run at least five experiments.
- **Termination:** Terminate the run if the goal state isn't reached even after some time τ has passed (consider τ = 10 minutes; modify as required).

## Useful Links
- [Branch and Bound](https://en.wikipedia.org/wiki/Branch_and_bound)
- [Iterative Deepening A*](https://en.wikipedia.org/wiki/Iterative_deepening_A*)
- [Hill Climbing](https://en.wikipedia.org/wiki/Hill_climbing)
- [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
- [Frozen Lake Environment](https://gymnasium.farama.org/environments/toy_text/frozen_lake/)
- [Ant Maze Environment](https://robotics.farama.org/envs/maze/ant_maze/)
- [Traveling Salesman Problem Environment](https://github.com/g-dendiev/gym_TSP)

