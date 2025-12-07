import heapq
import itertools
import math
from collections import defaultdict
from typing import Optional

import numpy as np

from utils import read_input, CoordTuple, DijkstraDistances, CoordGenerator


def modified_shortest_path_dijkstra(
    start: CoordTuple,
    grid: np.ndarray,
    flip_check: bool = True,
    end: Optional[CoordTuple] = None,
) -> DijkstraDistances:
    # Create neighbor grid
    dict_nn = _create_neighbors_dict(grid)

    # Initialise distance dictionary and visited set
    dists: DijkstraDistances = defaultdict(lambda: math.inf, {start: 0})
    visited = set()

    # Initialise queue
    queue: list[tuple[float, CoordTuple]] = [(0, start)]

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
            check = (
                grid[neighbor] - grid[current_node] > 1
                if flip_check
                else grid[neighbor] - grid[current_node] < -1
            )
            if check:
                new_dist = math.inf
            else:
                new_dist = current_dist + 1
            # Only consider this new path if it's better than any path we've
            # already found
            if new_dist < dists[neighbor]:
                dists[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))

    return dists


def _get_neighbors(node: CoordTuple, bounds: dict[str, CoordTuple]) -> CoordGenerator:
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


def _create_neighbors_dict(
    grid: np.ndarray,
) -> dict[CoordTuple, list[CoordTuple]]:
    """Create dictionary of neighbors for a grid"""
    dict_nn: dict[CoordTuple, list[CoordTuple]] = {
        (node[0], node[1]): []
        for node in list(itertools.product(range(grid.shape[0]), range(grid.shape[1])))
    }
    bounds = {"x": (0, grid.shape[0]), "y": (0, grid.shape[1])}
    for node in dict_nn.keys():
        dict_nn[node] = list(_get_neighbors(node, bounds))

    return dict_nn


def main(filename: str):
    grid_input = [[*line] for line in read_input(filename, line_strip=True)]
    # Find coordinates of starting and end points
    for i, line in enumerate(grid_input):
        for j, char in enumerate(line):
            if char == "S":
                start = (i, j)
                grid_input[i][j] = "a"
            elif char == "E":
                end = (i, j)
                grid_input[i][j] = "z"
    # Convert grid to integers
    grid_input = [[ord(char) - 97 for char in line] for line in grid_input]

    X = np.array(grid_input, dtype=np.int64)
    # Find shortest path
    shortest_path = modified_shortest_path_dijkstra(start, X, True, end)[end]
    print(f"Result of part 1: {shortest_path}")
    # Find all paths
    all_paths = modified_shortest_path_dijkstra(end, X, flip_check=False)
    # Find the lowest elevation squares
    x_coords, y_coords = np.where(X == 0)
    # Find min distance
    dist = math.inf
    for coords in zip(x_coords, y_coords):
        dist = min(dist, all_paths[coords])
    print(f"Result of part 2: {dist}")


if __name__ == "__main__":
    main("2022/12/input.txt")
