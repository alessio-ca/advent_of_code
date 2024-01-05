from utils import CoordTuple, timefunc
from typing import Dict, List, Set
from collections import defaultdict
from functools import lru_cache
import numpy as np
import heapq
import itertools
import math


@lru_cache(maxsize=None)
def manhattan(point: CoordTuple, source: CoordTuple) -> CoordTuple:
    return sum(abs(val1 - val2) for val1, val2 in zip(point, source))


def shortest_path_astar(
    start: CoordTuple,
    dict_nn: Dict[CoordTuple, List[CoordTuple]],
    dict_blizzards: Dict[int, List[CoordTuple]],
    grid_period: int,
    end: CoordTuple,
    start_time: int,
) -> int:
    # A node is a tuple (t,pos)
    start_node = (0, start)
    # Dictionary keeping track of the best guess
    #  as to how cheap a path could be from start to finish if it goes through node
    #  use Manhattan distance to end as heuristic
    heur_dict = defaultdict(lambda: math.inf, {start_node: manhattan(start, end)})
    # Min-Heap queue of nodes to process
    queue = [(heur_dict[start_node], start_node)]
    # Points (t,pos) already visited
    visited = set()
    while queue:
        # Pop the element of the queue with the shortest
        # estimated distance to goal - ignore if already visited
        _, (current_time, current_node) = heapq.heappop(queue)
        if (current_time, current_node) in visited:
            continue
        visited.add((current_time, current_node))
        # If we arrived at the end node,
        # return the shortest time
        if current_node == end:
            return current_time

        # Advance time & move blizzards if not already cached
        new_time = current_time + 1

        # Check all neighbors & the current node (in case we wait)
        for neighbor in dict_nn[current_node] + [current_node]:
            # Only consider candidate if not on a blizzard
            if neighbor not in dict_blizzards[(start_time + new_time) % grid_period]:
                heur_dict[(new_time, neighbor)] = new_time + manhattan(neighbor, end)
                # Add to queue
                heapq.heappush(
                    queue,
                    (
                        heur_dict[(new_time, neighbor)],
                        (new_time, neighbor),
                    ),
                )


def _create_periodic(x, i, vec, bound):
    x_t = (x + i * vec) % bound
    if x_t < 1:
        x_t += bound
    return x_t


def create_blizzards_lookups(
    grid: np.ndarray, grid_period: int
) -> Dict[int, Set[CoordTuple]]:
    # Create a dictionary with the blizzards position for each time step
    # Since we have periodicity over the valley, lcm(grid_x - 2, grid_y - 2)
    # gives the number of unique maps possible (since it guarantees we have
    #  cycled over all possible xy options)
    dict_blizzards = defaultdict(set)
    for arrow, vector in zip([">", "v", "<", "^"], [(0, 1), (1, 0), (0, -1), (-1, 0)]):
        # Get blizzard positions
        x_b, y_b = (grid == arrow).nonzero()
        for x, y in zip(x_b, y_b):
            for i in range(grid_period):
                x_t = _create_periodic(x, i, vector[0], grid.shape[0] - 2)
                y_t = _create_periodic(y, i, vector[1], grid.shape[1] - 2)
                dict_blizzards[i].add((x_t, y_t))

    return dict_blizzards


def _get_neighbors(
    node: CoordTuple, bounds: Dict[str, CoordTuple], grid: np.ndarray
) -> List[CoordTuple]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered."""
    x, y = node
    list_nn = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = (x + dx, y + dy)
        if (
            bounds["x"][0] <= xx < bounds["x"][1]
            and bounds["y"][0] <= yy < bounds["y"][1]
            and grid[(xx, yy)] != "#"
        ):
            list_nn.append((xx, yy))
    return list_nn


def create_neighbors_dict(
    grid: np.ndarray,
) -> Dict[CoordTuple, List[CoordTuple]]:
    """Create dictionary of neighbors for a grid"""
    dict_nn = {
        node: []
        for node in list(itertools.product(range(grid.shape[0]), range(grid.shape[1])))
    }
    bounds = {"x": (0, grid.shape[0]), "y": (0, grid.shape[1])}
    for node in dict_nn.keys():
        dict_nn[node] = _get_neighbors(node, bounds, grid)

    return dict_nn


@timefunc
def main(filename: str):
    grid = np.genfromtxt(filename, comments=None, delimiter=1, dtype=str)
    grid_period = np.lcm(grid.shape[0] - 2, grid.shape[1] - 2)
    dict_blizzards = create_blizzards_lookups(grid, grid_period)
    dict_nn = create_neighbors_dict(grid)
    start = (0, 1)
    end = (grid.shape[0] - 1, grid.shape[1] - 2)
    res_1 = shortest_path_astar(start, dict_nn, dict_blizzards, grid_period, end, 0)
    print(f"Result of part 1: {res_1}")
    res_2 = shortest_path_astar(end, dict_nn, dict_blizzards, grid_period, start, res_1)
    res_3 = shortest_path_astar(
        start, dict_nn, dict_blizzards, grid_period, end, res_1 + res_2
    )
    print(f"Result of part 2: {res_1 + res_2 + res_3}")


if __name__ == "__main__":
    main("2022/24/input.txt")
