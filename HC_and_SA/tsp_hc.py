"""
Assignment 2: Search and Optimization

Team Members
CS24M101 - A sai jagadeesh
CS24M111 - G Kavyasri
-------------------------------------
TSP Hill Climbing Solver
-------------------------------------
This script implements the Hill Climbing algorithm for the Traveling Salesman Problem (TSP).
It reads a .tsp file from the 'problems' folder of the cloned MicheleCattaneo/ant_colony_opt_TSP 
repository (e.g.,eil76.tsp,ch130.tsp, d198.tsp, etc.) and runs 5 Hill Climbing experiments.

"""

# Importing required libraries
import os
import math
import random
import time
import matplotlib.pyplot as plt
import imageio.v2 as imageio

# Parsing the TSP file to get city coordinates
def parse_tsp_file(filepath):
    cities = []
    reading = False
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.upper().startswith("NODE_COORD_SECTION"):
                reading = True
                continue
            if line.upper().startswith("EOF"):
                break
            if reading:
                parts = line.split()
                if len(parts) >= 3:
                    cities.append((float(parts[1]), float(parts[2])))
    return cities

# Calculating total route distance using Euclidean distance 
def total_distance(route, cities):
    dist = 0.0
    n = len(route)
    for i in range(n):
        x1, y1 = cities[route[i]]
        x2, y2 = cities[route[(i + 1) % n]]
        dist += math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist

# Plotting the TSP route and saving the image
def plot_route(cities, route, filename, title="TSP Route"):
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    route_coords = [cities[i] for i in route] + [cities[route[0]]]
    xs, ys = zip(*route_coords)
    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, marker='o')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(filename)
    plt.close()

# Creating a GIF from saved snapshots
def create_gif(snapshot_folder, gif_filename, duration=0.3):
    if not os.path.exists(snapshot_folder):
        print("Snapshot folder does not exist:", snapshot_folder)
        return
    images = [os.path.join(snapshot_folder, f) for f in sorted(os.listdir(snapshot_folder))
              if f.endswith(".png") and f.startswith("iter_")]
    if not images:
        print("No snapshots found in:", snapshot_folder)
        return
    frames = [imageio.imread(img) for img in images]
    out_dir = os.path.dirname(gif_filename)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
    imageio.mimsave(gif_filename, frames, duration=duration)
    print("GIF saved at:", gif_filename)

# Hill Climbing algorithm for TSP
def hill_climbing(cities, max_iterations=10000, time_limit=600, snapshot_callback=None): #time-limit = 10 mins
    start_time = time.time()
    n = len(cities)
    current_route = list(range(n))
    random.shuffle(current_route)
    current_cost = total_distance(current_route, cities)
    best_route = current_route[:]
    best_cost = current_cost
    iter_of_best = 0

    if snapshot_callback:
        snapshot_callback(best_route, 0)

    iteration = 0
    while iteration < max_iterations and (time.time() - start_time) < time_limit:
        neighbor = current_route[:]
        i, j = random.sample(range(n), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_cost = total_distance(neighbor, cities)
        if neighbor_cost < current_cost:
            current_route = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_route = current_route[:]
                best_cost = current_cost
                iter_of_best = iteration
                if snapshot_callback:
                    snapshot_callback(best_route, iteration)
        iteration += 1

    #calculating run time taken
    runtime = time.time() - start_time
    return best_route, best_cost, iter_of_best, iteration, runtime

# Running multiple Hill Climbing experiments (here 5 times)
def run_experiments(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp", num_runs=5,
                    max_iterations=10000, time_limit=600, plots_dir="results/plots"):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    cities = parse_tsp_file(tsp_file)
    print(f"Parsing TSP file: {tsp_file}")
    print(f"Number of cities: {len(cities)}\n")
    print("Running Hill Climbing for TSP...\n")
    best_costs = []
    run_times = []

    for run in range(1, num_runs + 1):
        route, cost, iter_best, total_iter, runtime = hill_climbing(cities, max_iterations, time_limit)
        best_costs.append(cost)
        run_times.append(runtime)
        print(f"Run {run}: Best Cost = {cost:.2f}, Found at Iteration: {iter_best}, Total Iterations = {total_iter}, Time = {runtime:.2f}s")
        plot_filename = os.path.join(plots_dir, f"hc_run_{run}_route.png")
        plot_route(cities, route, plot_filename, title=f"Run {run}: Best Cost = {cost:.2f}")

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, num_runs + 1), best_costs, marker='o')
    plt.title("Best Cost per Run")
    plt.xlabel("Run")
    plt.ylabel("Cost")
    plt.subplot(1, 2, 2)
    plt.plot(range(1, num_runs + 1), run_times, marker='o', color="orange")
    plt.title("Run Time per Experiment")
    plt.xlabel("Run")
    plt.ylabel("Time (s)")
    plt.tight_layout()
    summary_path = os.path.join(plots_dir, "hc_performance_summary.png")
    plt.savefig(summary_path)
    plt.show()

    print(f"\nAverage Best Cost over {num_runs} HC runs: {sum(best_costs) / num_runs:.2f}")
    print(f"Average Time over {num_runs} HC runs: {sum(run_times) / num_runs:.2f}s")

# using a snapshot experiment to create an animated GIF
def run_snapshot_experiment(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp",
                            max_iterations=10000, time_limit=600,
                            plots_dir="results/plots", gifs_dir="results/gifs"):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    if not os.path.exists(gifs_dir):
        os.makedirs(gifs_dir)
    snapshot_folder = os.path.join(plots_dir, "hc_snapshots")
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    cities = parse_tsp_file(tsp_file)
    
    print("Starting snapshot-enabled Hill Climbing for generating GIF...\n")
    def snapshot_callback(route, iteration):
        snap_path = os.path.join(snapshot_folder, f"iter_{iteration:05d}.png")
        plot_route(cities, route, snap_path, title=f"Iteration {iteration}")

    route, cost, iter_best, total_iter, runtime = hill_climbing(cities, max_iterations, time_limit, snapshot_callback)
    final_plot = os.path.join(plots_dir, "hc_final_route.png")
    plot_route(cities, route, final_plot, title="Final Route (Snapshot)")
    print(f"Snapshot Experiment Results:\n Best Cost = {cost:.2f},\n Found at Iteration = {iter_best},\n Total Iterations = {total_iter},\n Time = {runtime:.2f}s\n")
    gif_path = os.path.join(gifs_dir, "hill_climbing_animation.gif")
    create_gif(snapshot_folder, gif_path, duration=0.3)

# Main function
if __name__ == "__main__":
    random.seed(42)
    run_experiments(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp", num_runs=5, max_iterations=10000, time_limit=600, plots_dir="results/plots")
    run_snapshot_experiment(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp", max_iterations=10000, time_limit=600, plots_dir="results/plots", gifs_dir="results/gifs")
