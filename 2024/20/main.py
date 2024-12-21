from utils import (
    read_input,
    CoordTuple,
    get_neighbors,
    ConstraintFunArgs,
    ConstraintFun,
)
import numpy as np
import heapq
from collections import defaultdict, Counter
from itertools import product
import math
from typing import Generator


def manhattan(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


def constraint_track(fun_args: ConstraintFunArgs) -> bool:
    """Define constraint for neighbors"""
    xx, yy, _, _, grid = fun_args
    # Return False if neigh is a wall node
    return grid[xx, yy] != "#"


def shortest_path_dijkstra(
    start: CoordTuple, end: np.ndarray, grid: np.ndarray
) -> dict[CoordTuple, int]:
    """Dijkstra's algo for shortest path calculation between a start and any node.
    Returns a dict of shortest path length per node"""

    # Normal mode: track constraint
    constraint_fun = constraint_track

    # Initialise distance dictionary and visited set
    dists = defaultdict(lambda: math.inf, {start: 0})
    visited = set()

    # Initialise queue
    queue = [(0, start)]
    heapq.heapify(queue)

    while queue:
        # Pop the element of the queue with the shortest distance
        dist, node = heapq.heappop(queue)

        if node == end:
            continue
        # Nodes can get added to the priority queue multiple times. We only
        # process a node the first time we remove it from the priority queue.
        if node in visited:
            continue

        visited.add(node)

        for neighbor in get_neighbors(node, grid, constraint=constraint_fun):
            new_dist = dist + 1
            # Only consider this new path if it's better than any path we've
            # already found
            if new_dist < dists[neighbor]:
                dists[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))

    return dists


def get_nth_neighbors(
    node: CoordTuple,
    grid: np.ndarray,
    n: int,
    constraint: ConstraintFun = constraint_track,
) -> Generator[tuple[int, int, int], None, None]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered. Obstacles/constraints are considered"""
    x, y = node
    for dx, dy in product(range(-n, n + 1), repeat=2):
        if (dist := manhattan((0, 0), (dx, dy))) <= n:
            xx, yy = (x + dx, y + dy)
            # Check if out of bounds
            if 0 <= xx < grid.shape[0] and 0 <= yy < grid.shape[1]:
                # Check constraint
                if constraint((xx, yy, x, y, grid)):
                    yield xx, yy, dist


def find_cheats(start_paths, end_paths, grid, best_time, max_length) -> Counter:
    cheats = Counter()
    # Filter start and end paths to be at most:
    #  best_time
    #  - 100 (need to be 100 faster)
    #  - 2 (in and out for a single cheat)
    #  (to account for the two moves to enter and exit)
    start_paths = {
        node: dist for node, dist in start_paths.items() if dist <= best_time - 100 - 2
    }
    end_paths = {
        node: dist for node, dist in end_paths.items() if dist <= best_time - 100 - 2
    }
    for start_cheat in start_paths:
        for xx, yy, dist in get_nth_neighbors(start_cheat, grid, max_length):
            if (xx, yy) in end_paths:
                time_save = best_time - (
                    start_paths[start_cheat] + end_paths[(xx, yy)] + dist
                )
                if time_save > 0:
                    cheats[time_save] += 1
    return cheats


def main(filename: str):
    grid = np.array(list(map(list, read_input(filename))), dtype=str)
    start = tuple(np.transpose((grid == "S").nonzero())[0])
    end = tuple(np.transpose((grid == "E").nonzero())[0])

    # Find best paths from start to any node
    start_paths = shortest_path_dijkstra(start, end, grid)
    # Find best paths from end to any node
    end_paths = shortest_path_dijkstra(end, start, grid)

    # Obtain the pairs of valid_cheats that are at most 2 units apart
    cheats = find_cheats(start_paths, end_paths, grid, start_paths[end], 2)
    res = sum(count for cheat, count in cheats.items() if cheat >= 100)
    print(f"Result of part 1: {res}")
    # Obtain the pairs of valid_cheats that are at most 20 units apart
    cheats = find_cheats(start_paths, end_paths, grid, start_paths[end], 20)
    res = sum(count for cheat, count in cheats.items() if cheat >= 100)
    print(f"Result of part 2: {res}")


if __name__ == "__main__":
    main("2024/20/input.txt")
