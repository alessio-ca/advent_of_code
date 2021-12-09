from utils import read_input
import numpy as np
import itertools


def calculate_basin(i: int, j: int, X: np.ndarray) -> int:
    """Recursive function to calculate the basin size"""
    # If location has height 9 or has been already visited (height -1), return 0
    if X[i, j] == 9 or X[i, j] == -1:
        return 0

    # Mark current height location as -1 (visited)
    X[i, j] = -1

    # Generate possible neighbors
    neighbors = list(itertools.product([i - 1, i + 1], [j])) + list(
        itertools.product([i], [j - 1, j + 1])
    )
    # Contrain neighbors bounds
    neighbors = [
        pair
        for pair in neighbors
        if (pair[0] >= 0)
        & (pair[0] < X.shape[0])
        & (pair[1] >= 0)
        & (pair[1] < X.shape[1])
    ]
    # Recursive call
    return 1 + sum(calculate_basin(ii, jj, X) for ii, jj in neighbors)


def main():
    input_file = read_input("2021/09/input.txt")
    X = np.array([[int(x) for x in line] for line in input_file], dtype=int)
    # Initialize mask of ones
    mask = np.ones(X.shape, dtype=int)

    # Construct mask. Visiting each position, the mask is converted to 0 if any of the
    #  neighbors is lower than the current position. Implemented in a vectorized manner.
    # Loop over rows
    for i in range(1, X.shape[0]):
        # Top
        mask[i, :] = (X[i - 1, :] > X[i, :]) * mask[i, :]
        # Bottom
        mask[i - 1, :] = (X[i, :] > X[i - 1, :]) * mask[i - 1, :]
    # Loop over columns
    for i in range(1, X.shape[1]):
        # Left
        mask[:, i] = (X[:, i - 1] > X[:, i]) * mask[:, i]
        # Right
        mask[:, i - 1] = (X[:, i] > X[:, i - 1]) * mask[:, i - 1]

    print(f"Result of part 1: {((X + 1) * mask).sum()}")

    # Get indices of non null elements in mask
    low_idx = np.argwhere(mask == 1)

    # Calculate basin sizes
    sizes = []
    for i, j in low_idx:
        X_temp = X.copy()
        sizes.append(calculate_basin(i, j, X_temp))
    print(f"Result of part 2: {np.prod(sorted(sizes)[-3:])}")


if __name__ == "__main__":
    main()
