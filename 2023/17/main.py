import heapq
import itertools
import math
from collections import defaultdict
from typing import Optional

import numpy as np

from utils import read_input, timefunc, CoordTuple


def _get_neighbors(node: CoordTuple, bounds: dict[str, CoordTuple]) -> list[CoordTuple]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered."""
    x, y = node
    nn = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = (x + dx, y + dy)
        if (
            bounds["x"][0] <= xx < bounds["x"][1]
            and bounds["y"][0] <= yy < bounds["y"][1]
        ):
            nn.append((xx, yy))
    return nn


def create_neighbors_dict(
    grid: np.ndarray,
) -> dict[CoordTuple, list[CoordTuple]]:
    """Create dictionary of neighbors for a grid"""
    dict_nn: dict[CoordTuple, list[CoordTuple]] = {
        node: []
        for node in list(itertools.product(range(grid.shape[0]), range(grid.shape[1])))
    }
    bounds = {"x": (0, grid.shape[0]), "y": (0, grid.shape[1])}
    for node in dict_nn.keys():
        dict_nn[node] = _get_neighbors(node, bounds)

    return dict_nn


def shortest_path_dijkstra(
    start: CoordTuple,
    grid: np.ndarray,
    dict_nn: dict[CoordTuple, list[CoordTuple]],
    max_straight: int,
    min_straights: int,
    end: Optional[CoordTuple] = None,
) -> int:
    """Dijkstra's algo for shortest path calculation between a start node and any other
     node in a grid.
    Returns a dictionary of {node: distance} from the source node.

    `grid` specifies the weights associated to each node (here, a coordinate tuple)
    `dict_nn` contains the list of neighbors for each node
    `max_straight` and `min_straight` are the requirements for the problem
    If an optional `end` node is specified, calculation is performed down to the `end`
     node only (ignoring the rest of the grid for efficiency) and a single-element
      dictionary is returned.
    """

    # Initialise distance dictionary and visited set
    dists = defaultdict(lambda: math.inf, {(start, start, 0): 0.0})
    visited = set()

    # Initialise queue
    queue = [(0, start, start, 0)]

    while queue:
        # Pop the element of the queue with the shortest distance
        current_dist, current_node, previous_node, straights = heapq.heappop(queue)

        # If we arrived at the end node, return the dists dictionary
        if current_node == end:
            if straights >= min_straights:
                return current_dist
            else:
                continue

        # Nodes can get added to the priority queue multiple times. We only
        # process a node the first time we remove it from the priority queue.
        if (current_node, previous_node, straights) in visited:
            continue

        visited.add((current_node, previous_node, straights))

        for neighbor in dict_nn[current_node]:
            if neighbor != previous_node:
                new_straights = update_straights(neighbor, previous_node, straights)
                if new_straights <= max_straight and (  # Check max straight constraint
                    (new_straights - straights) > 0 or (straights >= min_straights)
                ):  # check min straights constraint
                    new_dist = current_dist + grid[neighbor]
                    # Only consider this new path if it's better than any path we've
                    # already found
                    if new_dist < dists[(neighbor, current_node, new_straights)]:
                        dists[(neighbor, current_node, new_straights)] = new_dist
                        heapq.heappush(
                            queue, (new_dist, neighbor, current_node, new_straights)
                        )
    return -1


def add_tuples(x, y):
    return (x[0] + x[1], y[0] + y[1])


def update_straights(neighbor, previous_node, straights):
    # If current node is on a straight course, the difference between the
    # previous and next node on one coordinate is always gonna be 0
    if neighbor[0] == previous_node[0] or neighbor[1] == previous_node[1]:
        return straights + 1
    # If not straight, reset count
    else:
        return 1


@timefunc
def main(filename: str):
    grid = np.array(
        list(list(map(int, row)) for row in read_input(filename)),
        dtype=int,
    )
    dict_nn = create_neighbors_dict(grid)
    # Perform shortest path search
    start = (0, 0)
    end = (grid.shape[0] - 1, grid.shape[1] - 1)
    print(
        f"Result of part 1: {shortest_path_dijkstra(start, grid, dict_nn, 3, 0, end)}"
    )
    print(
        f"Result of part 2: {shortest_path_dijkstra(start, grid, dict_nn, 10, 4, end)}"
    )


if __name__ == "__main__":
    main("2023/17/input.txt")
