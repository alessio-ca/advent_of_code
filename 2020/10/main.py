from functools import reduce

import numpy as np


def main():
    X = np.loadtxt("2020/10/input.txt", dtype="int")
    # Prepend 0 and the output adapter
    X = np.concatenate([[0], X, [X.max() + 3]])
    # Sort
    X = np.sort(X)

    # The only way to use all the adapters is to go in order of voltage
    # So, simply Count 1-jolt and 3-jolt differences
    one_jolt = (np.diff(X) == 1).sum()
    three_jolt = (np.diff(X) == 3).sum()
    print(f"Result of part 1: {one_jolt * three_jolt}")

    # To count the number of possible paths, we use DP
    path_count = np.zeros(shape=(X.max() + 1,), dtype="int")
    path_count[0] = 1
    for adapter in X:
        # Create 3 masks: True if the adapters with 1-3 less joltage
        #  are available
        masks = [X == (adapter - j) for j in [1, 2, 3]]
        # Combine into a single mask
        mask = reduce(np.logical_or, masks)
        # Update the path_count of the adapter with
        # the sum of the number of paths in the available adapters
        path_count[adapter] += path_count[X[mask]].sum()
    print(f"Result of part 2: {path_count[-1]}")


if __name__ == "__main__":
    main()
