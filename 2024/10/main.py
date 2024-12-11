from utils import read_input, CoordTuple
import numpy as np
from typing import Generator
from collections import deque, Counter


def _get_neighbors(
    node: CoordTuple, grid: np.ndarray
) -> Generator[CoordTuple, None, None]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered. Obstacles/constraints are considered"""
    x, y = node
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = (x + dx, y + dy)
        # Check if out of bounds
        if 0 <= xx < grid.shape[0] and 0 <= yy < grid.shape[1]:
            # Check if constraint
            if (grid[xx, yy] - grid[x, y]) == 1:
                yield (xx, yy)


def trailing_path(
    start: CoordTuple,
    grid: np.ndarray,
) -> int:
    """DFS for trailing path calculation.
    Allows for node revisit"""

    # Initialise queue
    stack = deque([(0, start)])
    # Initialise endpoints counter
    endpoints = Counter()

    while stack:
        # Pop from the stack & explore neighbors
        dist, head = stack.pop()
        for neighbor in _get_neighbors(head, grid):
            # Add to stack
            stack.append((dist + 1, neighbor))

        # Increase counter
        if dist == 9:
            endpoints[head] += 1
    return len(endpoints), sum(endpoints.values())


def main(filename: str):
    topomap = np.array(
        list(
            map(
                lambda line: list(map(int, (c if c != "." else -2 for c in line))),
                read_input(filename),
            )
        ),
        dtype=int,
    )
    res_1, res_2 = np.array(
        [trailing_path((x, y), topomap) for (x, y) in np.argwhere(topomap == 0)],
        dtype=int,
    ).sum(axis=0)
    print(f"Result of part 1: {res_1}")
    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main("2024/10/input.txt")
