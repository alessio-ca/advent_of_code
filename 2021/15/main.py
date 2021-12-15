from utils import read_input
import itertools
from typing import List, Tuple, Dict, Optional
import heapq
from collections import defaultdict

import numpy as np
import math


def shortest_path_dijkstra(
    start: Tuple[int, int],
    grid: np.ndarray,
    dict_nn: Dict[Tuple[int, int], List[Tuple[int, int]]],
    end: Optional[Tuple[int, int]] = None,
) -> Dict[Tuple[int, int], int]:
    """Dijkstra's algo for shortest path calculation between a start node and any other
     node in a grid.
    Returns a dictionary of {node: distance} from the source node.

    `grid` specifies the weights associated to each node (here, a coordinate tuple)
    `dict_nn` contains the list of neighbors for each node
    If an optional `end` node is specified, calculation is performed down to the `end`
     node only (ignoring the rest of the grid for efficiency) and a single-element
      dictionary is returned.
    """

    # Initialise distance dictionary and visited set
    dists = defaultdict(lambda: math.inf, {start: 0})
    visited = set()

    # Initialise queue
    queue = [(0, start)]

    while queue:
        # Pop the element of the queue with the shortest distance
        current_dist, current_node = heapq.heappop(queue)

        # If we arrived at the end node, return the dists dictionary
        if current_node == end:
            return defaultdict(lambda: math.inf, {end: current_dist})

        # Nodes can get added to the priority queue multiple times. We only
        # process a node the first time we remove it from the priority queue.
        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor in dict_nn[current_node]:
            new_dist = current_dist + grid[neighbor]
            # Only consider this new path if it's better than any path we've
            # already found
            if new_dist < dists[neighbor]:
                dists[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))

    return dists


def _get_neighbors(
    node: Tuple[int, int], bounds: Dict[str, Tuple[int, int]]
) -> List[Tuple[int, int]]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered."""
    x, y = node
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = (x + dx, y + dy)
        if (
            bounds["x"][0] <= xx < bounds["x"][1]
            and bounds["y"][0] <= yy < bounds["y"][1]
        ):
            yield xx, yy


def create_neighbors_dict(
    grid: np.ndarray,
) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """Create dictionary of neighbors for a grid"""
    dict_nn = {
        node: []
        for node in list(itertools.product(range(grid.shape[0]), range(grid.shape[1])))
    }
    bounds = {"x": (0, grid.shape[0]), "y": (0, grid.shape[1])}
    for node in dict_nn.keys():
        dict_nn[node] = _get_neighbors(node, bounds)

    return dict_nn


def enlarge_grid(grid: np.ndarray) -> np.ndarray:
    """Enlarge the grid"""
    large_grid = np.zeros(shape=(5 * grid.shape[0], 5 * grid.shape[1]), dtype=int)
    # Structure the first row block
    for i in range(5):
        slice_x = slice(grid.shape[0])
        slice_y = slice(i * grid.shape[1], (i + 1) * grid.shape[1])
        large_grid[slice_x, slice_y] = i + grid
    # For the other row blocks, simply add 1 to the previous block
    for i in range(1, 5):
        slice_x = slice(i * grid.shape[0], (i + 1) * grid.shape[0])
        up_slice_x = slice((i - 1) * grid.shape[0], i * grid.shape[0])
        large_grid[slice_x, :] = large_grid[up_slice_x, :] + 1

    # Wrap values around 9
    large_grid = large_grid % 9
    large_grid[large_grid == 0] = 9

    return large_grid


def main():
    input_file = read_input("2021/15/input.txt")
    grid = np.array([[int(num) for num in line] for line in input_file], dtype=int)

    # Create neighbour dictionary
    dict_nn = create_neighbors_dict(grid)

    # Perform shortest path search
    start = (0, 0)
    end = (grid.shape[0] - 1, grid.shape[1] - 1)
    res_dict = shortest_path_dijkstra(start, grid, dict_nn, end)
    print(f"Result of part 1: {res_dict[end]}")

    # For part 2, enlarge the grid
    large_grid = enlarge_grid(grid)

    # Create neighbour dictionary
    dict_nn = create_neighbors_dict(large_grid)

    # Perform shortest path search
    start = (0, 0)
    end = (large_grid.shape[0] - 1, large_grid.shape[1] - 1)
    res_dict = shortest_path_dijkstra(start, large_grid, dict_nn, end)
    print(f"Result of part 2: {res_dict[end]}")


if __name__ == "__main__":
    main()
