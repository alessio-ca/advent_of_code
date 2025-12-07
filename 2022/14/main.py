import itertools
from typing import Iterable, List, Set, Tuple

from utils import read_input


def pairwise(iterable: Iterable) -> Iterable:
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def construct_grid(raw_config: List[str]) -> Set[Tuple[int, int]]:
    # Convert to list of tuples
    rock_config = [
        [tuple(map(int, pair.split(","))) for pair in line.split("->")]
        for line in raw_config
    ]
    grid_set = set()
    for line in rock_config:
        # Create pairs
        pairs = pairwise(line)
        for pair in pairs:
            x1, y1 = pair[0]
            x2, y2 = pair[1]
            min_x, max_x = min([x1, x2]), max([x1, x2])
            min_y, max_y = min([y1, y2]), max([y1, y2])
            for coord in itertools.product(
                range(min_x, max_x + 1), range(min_y, max_y + 1)
            ):
                grid_set.add(coord)
    return grid_set


def grain_fall(grid, x, y, bounds):
    # Check boundary
    x_min, x_max, y_max = bounds
    if x_min:
        # We use all boundaries
        floor = False
        if not ((x > x_min) and (x < x_max) and (y < y_max)):
            raise StopIteration
    else:
        # We use floor
        floor = True

    # If floor is active, check floor
    if floor and (y + 1 == y_max + 2):
        # Rest
        grid.add((x, y))
        return None

    if (x, y + 1) in grid:
        # We hit something
        # Try left move
        if (x - 1, y + 1) not in grid:
            grain_fall(grid, x - 1, y, bounds)
        # Try right move
        elif (x + 1, y + 1) not in grid:
            grain_fall(grid, x + 1, y, bounds)
        # If nothing works, rest
        else:
            grid.add((x, y))
    else:
        # We didn't hit anything
        grain_fall(grid, x, y + 1, bounds)


def main(filename: str):
    raw_config = read_input(filename, line_strip=True)

    grid_set = construct_grid(raw_config)
    x, y = zip(*grid_set)
    bounds = min(x), max(x), max(y)
    i = 0
    while True:
        try:
            x_d, y_d = (500, 0)
            grain_fall(grid_set, x_d, y_d, bounds)
            i += 1
        except StopIteration:
            break
    print(f"Result of part 1: {i}")

    grid_set = construct_grid(raw_config)
    _, y = zip(*grid_set)
    bounds = None, None, max(y)
    i = 0
    while (500, 0) not in grid_set:
        x_d, y_d = (500, 0)
        grain_fall(grid_set, x_d, y_d, bounds)
        i += 1

    print(f"Result of part 2: {i}")


if __name__ == "__main__":
    main("2022/14/input.txt")
