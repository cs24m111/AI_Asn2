"""
Assignment 2: Search and Optimization

Team Members:
CS24M101 - A sai jagadeesh
CS24M111 - G Kavyasri
-----------------------------------------
TSP Simulated Annealing Solver
-----------------------------------------

This script implements the Simulated Annealing algorithm for the TSP.
It reads a .tsp file from the 'problems' folder and runs 5 SA experiments.
"""

# Imported required libraries
import os
import math
import random
import time
import matplotlib.pyplot as plt
import imageio.v2 as imageio

# Function for parsing the TSP file and extract city coordinates
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

#calculating the total distance of a route using euclidean distance
def total_distance(route, cities):
    dist = 0.0
    n = len(route)
    for i in range(n):
        x1, y1 = cities[route[i]]
        x2, y2 = cities[route[(i + 1) % n]]
        dist += math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist

# Function for plottinf the TSP route and saving the image
def plot_route(cities, route, filename, title="TSP Route via Simulated Annealing"):
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

#to create a GIF from saved snapshots
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

# Simulated Annealing algorithm for TSP
def simulated_annealing(cities, max_iterations=10000, time_limit=600, 
                          initial_temp=1000.0, cooling_rate=0.995, snapshot_callback=None):
    start_time = time.time()
    n = len(cities)
    current_route = list(range(n))
    random.shuffle(current_route)
    current_cost = total_distance(current_route, cities)
    best_route = current_route[:]
    best_cost = current_cost
    iter_of_best = 0
    temp = initial_temp

    if snapshot_callback:
        snapshot_callback(best_route, 0)

    iteration = 0
    while iteration < max_iterations and (time.time() - start_time) < time_limit and temp > 1e-8:
        neighbor = current_route[:]
        i, j = random.sample(range(n), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_cost = total_distance(neighbor, cities)
        delta = neighbor_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_route = current_route[:]
                best_cost = current_cost
                iter_of_best = iteration
                if snapshot_callback:
                    snapshot_callback(best_route, iteration)
        temp *= cooling_rate
        iteration += 1

    runtime = time.time() - start_time
    return best_route, best_cost, iter_of_best, iteration, runtime

# For running multiple SA experiments and plotting results (here runs=5)
def run_experiments(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp", num_runs=5,
                    max_iterations=10000, time_limit=600, plots_dir="results/plots"):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    print(f"\nParsing TSP file: {tsp_file}")
    cities = parse_tsp_file(tsp_file)
    print(f"Number of cities: {len(cities)}")

    best_costs = []
    run_times = []
    print("\nRunning Simulated Annealing for TSP...\n")
    for run in range(1, num_runs + 1):
        route, cost, iter_best, total_iter, runtime = simulated_annealing(
            cities, max_iterations=max_iterations, time_limit=time_limit
        )
        best_costs.append(cost)
        run_times.append(runtime)
        print(f"Run {run}: Best Cost = {cost:.2f}, Found at Iteration: {iter_best}, Total Iterations = {total_iter}, Time = {runtime:.2f}s")
        plot_filename = os.path.join(plots_dir, f"sa_run_{run}_route.png")
        plot_route(cities, route, plot_filename, title=f"SA Run {run}: Best Cost = {cost:.2f}")

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, num_runs + 1), best_costs, marker='o')
    plt.title("Best Cost per SA Run")
    plt.xlabel("Run")
    plt.ylabel("Cost")
    plt.subplot(1, 2, 2)
    plt.plot(range(1, num_runs + 1), run_times, marker='o', color="orange")
    plt.title("Run Time per SA Experiment")
    plt.xlabel("Run")
    plt.ylabel("Time (s)")
    plt.tight_layout()
    summary_path = os.path.join(plots_dir, "sa_performance_summary.png")
    plt.savefig(summary_path)
    plt.show()

    avg_cost = sum(best_costs) / num_runs
    avg_time = sum(run_times) / num_runs
    print(f"\nAverage Best Cost over {num_runs} SA runs: {avg_cost:.2f}")
    print(f"Average Time over {num_runs} SA runs: {avg_time:.2f}s")

#Using a snapshot experiment and generating a GIF
def run_snapshot_experiment(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp",
                            max_iterations=10000, time_limit=600,
                            plots_dir="results/plots", gifs_dir="results/gifs"):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    if not os.path.exists(gifs_dir):
        os.makedirs(gifs_dir)
    snapshot_folder = os.path.join(plots_dir, "sa_snapshots")
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)
    #print(f"\nParsing TSP file for SA snapshot run: {tsp_file}")
    cities = parse_tsp_file(tsp_file)
    #print(f"Number of cities: {len(cities)}")

    def snapshot_callback(route, iteration):
        snap_path = os.path.join(snapshot_folder, f"iter_{iteration:05d}.png")
        plot_route(cities, route, snap_path, title=f"SA Iteration {iteration}")

    print("\nStarting snapshot-enabled SA for generating GIF...\n")
    route, cost, iter_best, total_iter, runtime = simulated_annealing(
        cities, max_iterations=max_iterations, time_limit=time_limit, snapshot_callback=snapshot_callback
    )
    final_plot = os.path.join(plots_dir, "sa_final_route.png")
    plot_route(cities, route, final_plot, title="Final SA Route (Snapshot Experiment)")
    print(f"\nSA Snapshot Experiment Results:")
    print(f"  Best Cost: {cost:.2f}")
    print(f"  Found at Iteration: {iter_best}")
    print(f"  Total Iterations: {total_iter}")
    print(f"  Time: {runtime:.2f}s")
    gif_path = os.path.join(gifs_dir, "sa_animation.gif")
    create_gif(snapshot_folder, gif_path, duration=0.3)

# Main function to execute SA TSP problem
if __name__ == "__main__":
    random.seed(42)
    run_experiments(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp", num_runs=5,
                    max_iterations=10000, time_limit=600, plots_dir="results/plots")
    run_snapshot_experiment(tsp_file="ant_colony_opt_TSP/problems/eil76.tsp", max_iterations=10000,
                            time_limit=600, plots_dir="results/plots", gifs_dir="results/gifs")
