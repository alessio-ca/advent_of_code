import numpy as np
from utils import read_input


def part_1(grid: np.ndarray) -> int:
    x_size, y_size = grid.shape
    sum = 0
    # Iterate over 4 rotations of the grid (to catch all directions)
    for matrix in (np.rot90(grid, k=i) for i in range(4)):
        # Find valid seeds
        seeds = np.argwhere(matrix == "X")
        seeds = seeds[(seeds[:, 1] <= y_size - 4)]
        for seed in seeds:
            # Check that the row is XMAS
            x, y = seed
            if "".join(matrix[x, y : y + 4]) == "XMAS":
                sum += 1
            # Check that the diagonal of the 4x4 matrix is XMAS
            if x <= x_size - 4:
                if "".join(np.diag(matrix[x : x + 4, y : y + 4])) == "XMAS":
                    sum += 1
    return sum


def part_2(grid: np.ndarray) -> int:
    x_size, y_size = grid.shape
    sum = 0
    # Find valid seeds
    seeds = np.argwhere(grid == "A")
    seeds = seeds[
        (seeds[:, 1] <= y_size - 1)
        & (seeds[:, 1] >= 1)
        & (seeds[:, 0] <= x_size - 1)
        & (seeds[:, 0] >= 1)
    ]
    for seed in seeds:
        x, y = seed
        # Define 3x3 subgrid centered in A and the lr flip
        sub = grid[x - 1 : x + 2, y - 1 : y + 2]
        # Check that the two diagonals of sub are SAM or MAS
        if (("".join(np.diag(sub)) == "MAS") | ("".join(np.diag(sub)) == "SAM")) & (
            ("".join(np.diag(np.fliplr(sub))) == "MAS")
            | ("".join(np.diag(np.fliplr(sub))) == "SAM")
        ):
            sum += 1
    return sum


def main(filename: str):
    grid = np.array(list(map(list, read_input(filename))), dtype="U1")
    print(f"Result of part 1: {part_1(grid)}")
    print(f"Result of part 2: {part_2(grid)}")


if __name__ == "__main__":
    main("2024/04/input.txt")
