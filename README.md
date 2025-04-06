# AI Assignment 2: Search and Optimization

## Slide Deck
You can view the project slide deck [here](https://your-slide-deck-link.com).

## Algorithms Implemented
- **Branch and Bound**
- **Iterative Deepening A***
- **Hill Climbing**
- **Simulated Annealing**

## Environments Used 
- **For Branch and Bound & Iterative Deepening A*:**
  - Frozen Lake
- **For Hill Climbing & Simulated Annealing:**
  - Traveling Salesman Problem
   - This project implements Hill Climbing and Simulated Annealing algorithms for solving the Traveling Salesman Problem using the [ant_colony_opt_TSP](https://github.com/MicheleCattaneo/ant_colony_opt_TSP) environment.

-----------------------------------------------------------------------------------------------
## How to Run

### 1. For Branch and Bound
- **Clone the repository:**
  ```bash
  git clone <your-repo-url>
  ```
- **Navigate to the Branch and Bound directory:**
  ```bash
  cd branch_and_bound_directory
  ```
- **Run the program:**
  ```bash
  python branch_and_bound.py
  ```

### 2. For IDA*
- **Clone the repository:**
  ```bash
  git clone <your-repo-url>
  ```
- **Navigate to the IDA directory:**
  ```bash
  cd ida_star_directory
  ```
- **Run the program:**
  ```bash
  python ida_star.py
  ```

### 3. For Hill Climbing (HC) and Simulated Annealing (SA)
#### 3.1 Clone the Ant Colony Repository
- **Clone the repository:**
   - git clone <ant_colony_repo_url>
  ```bash
  git clone https://github.com/MicheleCattaneo/ant_colony_opt_TSP.git
  ```

#### 3.2 Setup Virtual Environment
- **Create a virtual environment:**
  ```bash
  python -m venv env
  ```

#### 3.3 Activate Virtual Environment
- **On Windows:**
  ```bash
  env\Scripts\activate
  ```
- **On macOS and Linux:**
  ```bash
  source env/bin/activate
  ```

#### 3.4 Install Necessary Libraries
- **Install required libraries:**
  ```bash
  pip install gym matplotlib imageio
  ```

#### 3.5 Run Hill Climbing (HC)
- **Execute the Hill Climbing algorithm:**
  ```bash
  python tsp_hc.py
  ```

#### 3.6 Run Simulated Annealing (SA)
- **Execute the Simulated Annealing algorithm:**
  ```bash
  python tsp_SA.py
  ```
--------------------------------------------------------------------------------------------------

## Useful Links
- [Branch and Bound](https://en.wikipedia.org/wiki/Branch_and_bound)
- [Iterative Deepening A*](https://en.wikipedia.org/wiki/Iterative_deepening_A*)
- [Hill Climbing](https://en.wikipedia.org/wiki/Hill_climbing)
- [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
- [Frozen Lake Environment](https://gymnasium.farama.org/environments/toy_text/frozen_lake/)
- [Ant Maze Environment](https://robotics.farama.org/envs/maze/ant_maze/)
- [Traveling Salesman Problem Environment](https://github.com/g-dendiev/gym_TSP)

