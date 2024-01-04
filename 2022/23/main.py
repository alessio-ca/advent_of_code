from utils import timefunc, CoordTuple
from scipy.ndimage import convolve
import numpy as np
from collections import deque, Counter
from typing import Tuple, Dict


CONV_FILTER = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)
S_FILTER = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=int)
N_FILTER = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]], dtype=int)
E_FILTER = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]], dtype=int)
W_FILTER = np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]], dtype=int)


def trim_zeros(arr: np.ndarray) -> np.ndarray:
    slices = tuple(slice(idx.min(), idx.max() + 1) for idx in np.nonzero(arr))
    return arr[slices]


def add_tuples(t1: CoordTuple, t2: CoordTuple) -> CoordTuple:
    return (t1[0] + t2[0], t1[1] + t2[1])


def perform_convolutions(grid: np.ndarray) -> Tuple[Dict[str, np.ndarray], np.ndarray]:
    # Perform 4 directional convolutions and a full one
    convs = {
        move: convolve(grid, d_filter, mode="constant")
        for move, d_filter in zip(
            ["N", "S", "W", "E"], [N_FILTER, S_FILTER, W_FILTER, E_FILTER]
        )
    }
    # Store sum of all directions - we don't care about double summations
    full_conv = sum(conv for conv in convs.values())
    return convs, full_conv


def enlarge_grid(grid):
    # Pad grid by 10
    grid = np.pad(grid, ((10, 10), (10, 10)))
    # Elves pos
    x_e, y_e = np.nonzero(grid)
    # Initialise lookup for elves
    lookup_elves = dict()
    for i, (x, y) in enumerate(zip(x_e, y_e)):
        lookup_elves[i] = (x, y)
    # Initialise convolutions
    convs, full_conv = perform_convolutions(grid)

    return grid, lookup_elves, convs, full_conv


def diffuse_elves(grid: np.ndarray) -> np.ndarray:
    grid, lookup_elves, convs, full_conv = enlarge_grid(grid)
    # Direction queue
    directions = deque([("N", (-1, 0)), ("S", (1, 0)), ("W", (0, -1)), ("E", (0, 1))])

    step = 0
    while any(full_conv[c] > 0 for c in lookup_elves.values()):
        step += 1
        # First half of round: propose move
        moves = []
        for i in lookup_elves:
            if full_conv[lookup_elves[i]] == 0:
                # Don't move
                moves.append((i, lookup_elves[i]))
            else:
                # Check which of the direction convolution filters returns 0
                # Use the direction queue
                for move, direction in directions:
                    if convs[move][lookup_elves[i]] == 0:
                        # Add move and break loop
                        moves.append((i, add_tuples(lookup_elves[i], direction)))
                        break
        # Second half of round: move
        # Filter move list so that only unique elements are preserved
        overlaps = Counter(t for _, t in moves)
        for e_id, t in moves:
            if overlaps[t] == 1:
                # Update grid as well
                grid[lookup_elves[e_id]] = 0
                lookup_elves[e_id] = t
                grid[lookup_elves[e_id]] = 1

        # Perform convolutions
        convs, full_conv = perform_convolutions(grid)
        # Rotate queue
        directions.rotate(-1)

        if step == 10:
            # Store result for part 1
            part_1_grid = trim_zeros(grid).copy()
        # If we reached the boundary, re-enlarge
        if any(
            [grid[0, :].sum(), grid[:, 0].sum(), grid[-1, :].sum(), grid[:, -1].sum()]
        ):
            grid, lookup_elves, convs, full_conv = enlarge_grid(grid)

    return part_1_grid, step + 1


@timefunc
def main(filename: str):
    grid = np.where(
        np.genfromtxt(filename, comments=None, delimiter=1, dtype=str) == "#", 1, 0
    )
    part_1_grid, part_2_num = diffuse_elves(grid)
    print(f"Result of part 1: {(part_1_grid == 0).sum()}")
    print(f"Result of part 2: {part_2_num}")


if __name__ == "__main__":
    main("2022/23/input.txt")
