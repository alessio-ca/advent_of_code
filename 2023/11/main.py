from utils import read_input
import numpy as np
import itertools


def get_galaxies(grid: np.ndarray, expansion_n: int) -> np.ndarray:
    # Get galaxies positions.
    # Consider expansion
    x_r, y_r = (grid == "#").nonzero()
    x = x_r.copy()
    y = y_r.copy()
    for i, row in enumerate(grid):
        if all(row == "."):
            x[x_r > i] += expansion_n - 1
    for i, column in enumerate(grid.T):
        if all(column == "."):
            y[y_r > i] += expansion_n - 1
    return x, y


def compute_distances(x: np.ndarray, y: np.ndarray) -> int:
    galaxies = list((x, y) for x, y in zip(x, y))
    res = 0
    for start, end in itertools.combinations(galaxies, 2):
        # Compute Manhattan Distance
        x0, y0 = start
        x1, y1 = end
        res += np.abs(x1 - x0) + np.abs(y1 - y0)
    return res


def main(filename: str):
    grid_raw = np.array([list(line) for line in read_input(filename)], dtype=str)
    # Get galaxies positions & compute
    x, y = get_galaxies(grid_raw, expansion_n=2)
    print(f"Result of part 1: {compute_distances(x,y)}")
    # Get galaxies positions & compute
    x, y = get_galaxies(grid_raw, expansion_n=1000000)
    print(f"Result of part 2: {compute_distances(x,y)}")


if __name__ == "__main__":
    main("2023/11/input.txt")
