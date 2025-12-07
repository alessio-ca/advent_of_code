from typing import Callable

import numpy as np

from utils import CoordTuple, diff_tuple, read_input


def check_bounds(x: int, y: int, xg: int, yg: int) -> bool:
    return x >= 0 and x < xg and y >= 0 and y < yg


def part_1_antinodes(
    xi: int, yi: int, xj: int, yj: int, xg: int, yg: int, antinodes: set[CoordTuple]
) -> None:
    (x, y) = diff_tuple((xi, yi), (xj, yj))
    if check_bounds(xi + x, yi + y, xg, yg):
        antinodes.add((xi + x, yi + y))
    if check_bounds(xj - x, yj - y, xg, yg):
        antinodes.add((xj - x, yj - y))


def part_2_antinodes(
    xi: int, yi: int, xj: int, yj: int, xg: int, yg: int, antinodes: set[CoordTuple]
) -> None:
    (x, y) = diff_tuple((xi, yi), (xj, yj))
    k = 0
    while check_bounds(xi + k * x, yi + k * y, xg, yg):
        antinodes.add((xi + k * x, yi + k * y))
        k += 1

    k = 0
    while check_bounds(xj - k * x, yj - k * y, xg, yg):
        antinodes.add((xj - k * x, yj - k * y))
        k += 1

    pass


def find_antinodes(
    map: np.ndarray,
    antenna_types: np.ndarray,
    antinodes_fun: Callable[[int, int, int, int, int, int, set[CoordTuple]], None],
) -> int:
    xg, yg = map.shape
    antinodes: set[CoordTuple] = set()
    for kind in antenna_types:
        antennas = np.argwhere(map == kind)
        for i, (xi, yi) in enumerate(antennas):
            for _, (xj, yj) in enumerate(antennas[i + 1 :]):
                antinodes_fun(xi, yi, xj, yj, xg, yg, antinodes)

    return len(antinodes)


def main(filename: str):
    map = np.array([list(line) for line in read_input(filename)], dtype=str)
    antenna_types = np.unique(map)
    antenna_types = antenna_types[antenna_types != "."]

    print(f"Result of part 1: {find_antinodes(map, antenna_types, part_1_antinodes)}")
    print(f"Result of part 2: {find_antinodes(map, antenna_types, part_2_antinodes)}")


if __name__ == "__main__":
    main("2024/08/input.txt")
