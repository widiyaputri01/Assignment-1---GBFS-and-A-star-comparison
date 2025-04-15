import heapq
import time
import random

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]
MOVES = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7]
}

def is_solvable(state):
    inv_count = 0
    for i in range(len(state)):
        for j in range(i+1, len(state)):
            if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                inv_count += 1
    return inv_count % 2 == 0

def generate_random_start():
    state = GOAL_STATE[:]
    while True:
        random.shuffle(state)
        if is_solvable(state):
            return state

def misplaced_tiles(state):
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != GOAL_STATE[i])

def get_neighbors(state):
    zero_index = state.index(0)
    neighbors = []
    for move in MOVES[zero_index]:
        new_state = state[:]
        new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
        neighbors.append(new_state)
    return neighbors

def gbfs_with_path(start):
    start_time = time.time()
    open_set = []
    heapq.heappush(open_set, (misplaced_tiles(start), start))
    visited = set()
    parent_map = {tuple(start): None}
    nodes_explored = 0

    while open_set:
        h, current = heapq.heappop(open_set)
        nodes_explored += 1
        visited.add(tuple(current))

        if current == GOAL_STATE:
            # Rekonstruksi path
            path = []
            state = tuple(current)
            while state is not None:
                path.append(state)
                state = parent_map[state]
            path.reverse()
            return time.time() - start_time, nodes_explored, len(path) - 1, path

        for neighbor in get_neighbors(current):
            neighbor_t = tuple(neighbor)
            if neighbor_t not in visited:
                parent_map[neighbor_t] = tuple(current)
                heapq.heappush(open_set, (misplaced_tiles(neighbor), neighbor))

    return time.time() - start_time, nodes_explored, -1, []

def run_gbfs_experiments(n=5):
    total_time = 0
    total_nodes = 0
    total_path_length = 0

    for i in range(1, n+1):
        start_state = generate_random_start()
        print(f"\nExperiment #{i}")
        print("Start State:")
        for j in range(0, 9, 3):
            print(start_state[j:j+3])

        time_taken, nodes, path_len, path = gbfs_with_path(start_state)

        total_time += time_taken
        total_nodes += nodes
        total_path_length += path_len

        print(f"Time: {time_taken * 1000:.2f} ms")
        print(f"Nodes explored: {nodes}")
        print(f"Path length: {path_len}")

    print("\nAverage Results over", n, "experiments:")
    print(f"Average Time: {total_time / n * 1000:.2f} ms")
    print(f"Average Nodes Explored: {total_nodes // n}")
    print(f"Average Path Length: {total_path_length // n}")

if __name__ == "__main__":
    run_gbfs_experiments()
