from utils import (
    read_input,
    ConstraintFunArgs,
    CoordTuple,
    ConstraintFun,
)
from collections import defaultdict
import heapq
import numpy as np
from typing import Optional, Generator
import math

VECTORS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def constraint(fun_args: ConstraintFunArgs) -> bool:
    """Define constraint for neighbors"""
    xx, yy, _, _, grid = fun_args
    return grid[xx, yy] != "#"


def get_neighbors(
    node: CoordTuple,
    grid: np.ndarray,
    constraint: ConstraintFun = constraint,
) -> Generator[tuple[CoordTuple, CoordTuple], None, None]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered. Obstacles/constraints are considered"""
    x, y = node
    for dx, dy in VECTORS:
        xx, yy = (x + dx, y + dy)
        # Check if out of bounds
        if 0 <= xx < grid.shape[0] and 0 <= yy < grid.shape[1]:
            # Check constraint
            if constraint((xx, yy, x, y, grid)):
                yield (xx, yy), (dx, dy)


class Path:
    def __init__(self):
        self.dist = math.inf
        self.path = set()


def modified_dijkstra(
    start: CoordTuple,
    grid: np.ndarray,
    end: Optional[CoordTuple] = None,
) -> tuple[int, set[CoordTuple]]:
    """Modified Dijkstra's algo for marking all nodes belonging to
    any shortest path in the graph,
    Returns a tuple of:
    - shortest distance
    - set of nodes belonging to shortest paths
    """

    # Initialise distance dictionary, having a (node,head): Path() structure
    # Each dictionary value is a Path object storing:
    # - The shortest distance to this (node,head) tuple
    # - The set of nodes belonging to the shortest paths so far
    dists: defaultdict[tuple[CoordTuple, CoordTuple], Path] = defaultdict(
        lambda: Path()
    )

    # Initialise queue - from start, moving east
    queue = [(0, start, (0, 1))]
    dists[(start, (0, 1))].dist = 0
    dists[(start, (0, 1))].path = {start}

    while queue:
        # Pop the element of the queue with the shortest distance
        dist, node, head = heapq.heappop(queue)

        # If we arrived at the end node, continue
        if node == end:
            continue

        for neigh, neigh_head in get_neighbors(node, grid, constraint):
            # Prevent 180 turns
            if neigh not in dists[(node, head)].path:
                # If direction is same, add 1
                if neigh_head == head:
                    new_dist = dist + 1
                # Else, Do a step & rotation
                else:
                    new_dist = dist + 1001
                # Only consider this new path if it's better to any path we've
                # found arriving in (neigh, neigh_head)
                if new_dist < dists[(neigh, neigh_head)].dist:
                    dists[(neigh, neigh_head)].dist = new_dist
                    dists[(neigh, neigh_head)].path = dists[(node, head)].path | {neigh}
                    heapq.heappush(queue, (new_dist, neigh, neigh_head))
                # If instead we have a duplicate best path, expand the existing path
                elif new_dist == dists[(neigh, neigh_head)].dist:
                    dists[(neigh, neigh_head)].path.update(dists[(node, head)].path)

    # Find minimum path among those arriving in end from different directions
    min_dist = min(dists[(end, head)].dist for head in VECTORS)
    path_tiles = set()
    for head in VECTORS:
        if dists[(end, head)].dist == min_dist:
            path_tiles.update(dists[(end, head)].path)
    return min_dist, path_tiles


def print_maze(dists, maze, node):
    for head in VECTORS:
        new_maze = maze.copy()
        for x, y in dists[(node, head)].path:
            new_maze[x][y] = "O"

        print(new_maze)


def main(filename: str):
    maze = np.array(list(map(list, read_input(filename))), dtype=str)
    start = (len(maze) - 2, 1)
    end = (1, len(maze[0]) - 2)
    dist, tiles = modified_dijkstra(start, maze, end)
    print(f"Result of part 1: {dist}")
    print(f"Result of part 1: {len(tiles)}")


if __name__ == "__main__":
    main("2024/16/input.txt")
