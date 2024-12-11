from utils import read_input, get_neighbors, CoordTuple, ConstraintFunArgs
import numpy as np
from collections import deque, Counter


def constraint(fun_args: ConstraintFunArgs) -> bool:
    """Define constraint for neighbors"""
    xx, yy, x, y, grid = fun_args
    return grid[xx, yy] - grid[x, y] == 1


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
        for neighbor in get_neighbors(head, grid, constraint):
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
