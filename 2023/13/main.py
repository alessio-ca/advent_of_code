from typing import Callable

import numpy as np

from utils import read_input_batch


def test_grid(grid, i):
    """Test if a grid is symmetric along axis 0 with measure i.
    Return two booleans,testing both top and bottom reflections"""
    return np.array_equal(grid[:i], np.flip(grid[i : 2 * i], axis=0)), np.array_equal(
        grid[-i:], np.flip(grid[-2 * i : -i], axis=0)
    )


def test_smudge(grid, i):
    """Test if a grid has a smudge, i.e. test if symmetry along axis 0
      with measure i is short of 1 element.
    Return two booleans,testing both top and bottom reflections"""
    return (grid[:i] == np.flip(grid[i : 2 * i], axis=0)).sum() == i * grid.shape[
        1
    ] - 1, (grid[-i:] == np.flip(grid[-2 * i : -i], axis=0)).sum() == i * grid.shape[
        1
    ] - 1


def find_reflection(grid: np.ndarray, condition: Callable) -> int:
    """Find the reflection along taxis 0 in a grid for a particular condition"""
    grid_x, _ = grid.shape
    i = int(grid_x / 2)
    while i > 0:
        test_1, test_2 = condition(grid, i)
        if test_1:
            break
        if test_2:
            i = grid_x - i
            break
        i -= 1
    return i


def test_pattern(grid, condition):
    # Test rows and columns
    return 100 * find_reflection(grid, condition) + find_reflection(grid.T, condition)


def main(filename: str):
    patterns = [
        np.array([list(row) for row in pattern]) == "#"
        for pattern in read_input_batch(filename)
    ]
    total = 0
    for pattern in patterns:
        total += test_pattern(pattern, test_grid)
    print(f"Result of part 1: {total}")

    total = 0
    for pattern in patterns:
        total += test_pattern(pattern, test_smudge)
    print(f"Result of part 2: {total}")


if __name__ == "__main__":
    main("2023/13/input.txt")
