import heapq
import math
from collections import defaultdict, deque

import numpy as np

from utils import ConstraintFunArgs, CoordTuple, diff_tuple, get_neighbors, read_input


def constraint(fun_args: ConstraintFunArgs) -> bool:
    """Define constraint for neighbors"""
    xx, yy, _, _, grid = fun_args
    return grid[xx, yy] == 0


def shortest_path_dijkstra(
    start: CoordTuple, end: CoordTuple, grid: np.ndarray
) -> set[CoordTuple]:
    """Dijkstra's algo for shortest path calculation between a start and end node.
    Returns the shortest path"""

    # Initialise distance dictionary and visited set
    dists = defaultdict(lambda: math.inf, {start: 0.0})
    visited = set()

    # Initialise queue
    queue = [(0, start, {start})]
    heapq.heapify(queue)

    while queue:
        # Pop the element of the queue with the shortest distance
        dist, node, path = heapq.heappop(queue)

        # If we arrived at the end node, return the end
        if node == end:
            return path

        # Nodes can get added to the priority queue multiple times. We only
        # process a node the first time we remove it from the priority queue.
        if node in visited:
            continue

        visited.add(node)

        for neighbor in get_neighbors(node, grid, constraint=constraint):
            new_dist = dist + 1
            # Only consider this new path if it's better than any path we've
            # already found
            if new_dist < dists[neighbor]:
                dists[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor, path | {neighbor}))

    return set()


def find_first_stop(
    bytes: list[CoordTuple], path: set[CoordTuple], grid: np.ndarray
) -> CoordTuple:
    remaining_bytes = deque(bytes)
    # Loop until a path exists
    start = (0, 0)
    end = diff_tuple(grid.shape, (1, 1))
    while path:
        yn, xn = remaining_bytes.popleft()
        # Add new byte to grid
        grid[xn, yn] = 1
        # If the new byte is on the path,
        # recalculate shortest path
        if (xn, yn) in path:
            path = shortest_path_dijkstra(start, end, grid)

    return (yn, xn)


def main(filename: str):
    input_str = filename.split("/")[-1]
    if "example" in input_str:
        i_bytes = 12
        space_size = 7
    else:
        i_bytes = 1024
        space_size = 71

    bytes: list[CoordTuple] = list(
        (
            map(lambda x: tuple(map(int, x.split(","))), read_input(filename))  # type: ignore
        )
    )

    grid = np.zeros(shape=(space_size, space_size), dtype="int")
    for y, x in bytes[:i_bytes]:
        grid[x, y] = 1

    start = (0, 0)
    end = diff_tuple(grid.shape, (1, 1))
    path = shortest_path_dijkstra(start, end, grid)
    print(f"Result of part 1: {len(path) - 1}")
    print(f"Result of part 2: {find_first_stop(bytes[i_bytes:], path, grid)}")


if __name__ == "__main__":
    main("2024/18/input.txt")
