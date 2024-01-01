from __future__ import annotations
from utils import read_input
import numpy as np
from typing import Tuple, Dict, List, Callable
import itertools
from collections import defaultdict


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def coord(self):
        return (self.x, self.y)

    def add(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)


def _get_neighbors(node: Point, bounds: Dict[str, Tuple[int, int]]) -> List[Point]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered."""
    for move in (Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)):
        neighbor = node.add(move)
        if (
            bounds["x"][0] <= neighbor.x < bounds["x"][1]
            and bounds["y"][0] <= neighbor.y < bounds["y"][1]
        ):
            yield neighbor


def _get_neighbors_infinite(
    node: Point, bounds: Dict[str, Tuple[int, int]]
) -> List[Point]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid is supposed to be periodic"""
    for move in (Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)):
        neighbor = node.add(move)
        # Scale
        neighbor.x -= bounds["x"][0]
        neighbor.y -= bounds["y"][0]
        # Shift
        neighbor.x %= bounds["x"][1] - bounds["x"][0]
        neighbor.y %= bounds["y"][1] - bounds["y"][0]
        # Return
        neighbor.x += bounds["x"][0]
        neighbor.y += bounds["y"][0]

        yield neighbor


def create_neighbors_dict(
    grid: np.ndarray, method: Callable
) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """Create dictionary of neighbors for a grid"""
    dict_nn = {
        node: []
        for node in list(itertools.product(range(grid.shape[0]), range(grid.shape[1])))
    }
    bounds = {"x": (0, grid.shape[0]), "y": (0, grid.shape[1])}
    for node in dict_nn.keys():
        dict_nn[node] = [
            nn.coord for nn in method(Point(*node), bounds) if grid[nn.coord] != "#"
        ]

    return dict_nn


def is_even(i):
    return i % 2 == 0


def check_plane(dp, p):
    if dp > 1:
        return p - 1
    elif dp < -1:
        return p + 1
    else:
        return p


def augment_plane(n_x, n_y, x, y, p_x, p_y):
    p_x = check_plane(n_x - x, p_x)
    p_y = check_plane(n_y - y, p_y)
    return p_x, p_y


def walk_loop(dict_nn, start, n_steps):
    # Walk the loop with constraints
    visited_even = set()
    visited_odd = set()
    dict_counts = defaultdict(list)
    # Each state is represented by the hyperplane coordinates and grid coordinates
    start_state = (0, 0, start.x, start.y)
    queue = {start_state}

    i = 0
    output_list = []
    # Loop until queue exhausts
    #  (no more possible new moves, relevant for a finite grid)
    while queue:
        i += 1
        # Break loop if exceeding problem steps
        if i > n_steps:
            i -= 1
            break
        next_queue = set()
        for px, py, x, y in queue:
            point = (x, y)
            # Examine neighbors
            for neigh in dict_nn[point]:
                nx, ny = neigh
                # Check if moving to next map (relevant for infinite grid)
                pxx, pyy = augment_plane(nx, ny, x, y, px, py)
                new_state = (pxx, pyy, nx, ny)
                # Split between even and odd
                if is_even(i):
                    if new_state not in visited_even:
                        next_queue.add(new_state)
                        visited_even.add(new_state)
                        dict_counts[(new_state, True)] = i
                else:
                    if new_state not in visited_odd:
                        next_queue.add(new_state)
                        visited_odd.add(new_state)
                        dict_counts[(new_state, False)] = i

        queue = next_queue
        if is_even(i):
            output_list.append(len(visited_even))
        else:
            output_list.append(len(visited_odd))

    return i, visited_even, visited_odd, dict_counts, output_list


def walk_grid(dict_nn, start, n_steps):
    i, visited_even, visited_odd, _, _ = walk_loop(dict_nn, start, n_steps)
    if is_even(i):
        return len(visited_even)
    else:
        return len(visited_odd)


def walk_infinite_grid(dict_nn, start, n_steps):
    _, _, _, dict_counts, output_list = walk_loop(dict_nn, start, n_steps)
    dict_result = defaultdict(list)
    for ((px, py, x, y), t), value in dict_counts.items():
        dict_result[(x, y)].append((px, py, t, value))

    return output_list


def search_result(period: int, steps: int, offset: int, y: np.ndarray):
    """Finds the periodic pattern by solving a quadratic equation.
    Both example and input have periodicity.
    The number of occupied tiles evolves based on three parameters:
    - The offset (when does the pattern emerge)
    - The period of the pattern
    - The number of steps
    """
    # The number of occupied tiles follows a quadratic equation after the offset.
    # Our target is the non-periodic end part.
    # We solve the following equation:
    # ax^2 + bx + c = i
    # The "i"s are chosen to be the number of occupied tiles at the offset
    #  and the next two periods.
    # The "x"s are the number of periods (0, 1, 2,...)
    # This will allow us to fit the relationship and extrapolate to target
    target = (steps - offset) // period
    idx = [
        offset,
        offset + period,
        offset + period * 2,
    ]
    coefficients = np.polyfit(np.arange(len(idx)), y[idx], 2)
    result = np.polyval(coefficients, target)
    return int(np.round(result))


def main(filename: str):
    grid = np.array([[c for c in line] for line in read_input(filename)], dtype=str)
    x_0, y_0 = (grid == "S").nonzero()
    start = Point(x_0[0], y_0[0])
    # Create neighbour dictionary
    dict_nn = create_neighbors_dict(grid, method=_get_neighbors)
    # Number of iterations changes based on example/input
    if grid.shape[0] < 20:
        i = 6
    else:
        i = 64
    print(f"Result of part 1: {walk_grid(dict_nn, start, i)}")
    dict_nn_infinite = create_neighbors_dict(grid, method=_get_neighbors_infinite)
    y = np.insert(
        np.array(walk_infinite_grid(dict_nn_infinite, start, 400), dtype=int),
        0,
        0,
    )
    # The second part relies on finding the periodic pattern.
    # The number of occupied tiles scales quadratically, given an offset and a base
    # These values have been found by investigating the input (see attached images)
    if grid.shape[0] < 20:
        base = 11
        steps = 5000
        offset = 39
    else:
        base = 131
        steps = 26501365
        offset = 65

    print(f"Result of part 2: {search_result(base,steps,offset,y)}")


if __name__ == "__main__":
    main("2023/21/example.txt")
