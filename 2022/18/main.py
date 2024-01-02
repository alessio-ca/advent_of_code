from utils import read_input
import numpy as np
from scipy import ndimage

EDGES = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]


def calculate_exposed_edges(cubes):
    n = 0

    for x, y, z in cubes:
        for dx, dy, dz in EDGES:
            if (x + dx, y + dy, z + dz) not in cubes:
                n += 1

    return n


def main(filename: str):
    lines = read_input(filename, line_strip=True)
    cubes = set(tuple(map(int, line.split(","))) for line in lines)
    print(f"Result of part 1: {calculate_exposed_edges(cubes)}")

    # Convert cubes to array
    cubes = np.array(
        [list(map(int, line.split(","))) for line in lines],
        dtype=np.int64,
    )
    # Create 3D space
    space = np.zeros(shape=cubes.max(axis=0) + 1, dtype=np.int64)
    xc, yc, zc = cubes.T
    space[xc, yc, zc] = 1
    # Fill holes
    space = ndimage.binary_fill_holes(space)
    # Reconstruct set of cubes from space
    cubes = set(zip(*np.where(space)))
    print(f"Result of part 2: {calculate_exposed_edges(cubes)}")


if __name__ == "__main__":
    main("2022/18/input.txt")
