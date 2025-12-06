from itertools import combinations

import numpy as np


def main():
    X = np.loadtxt("2020/01/input.txt", dtype=int)

    # For part 1, we can use vector intersection
    # Find the complement to 2020
    X_comp = 2020 - X
    # The entries that add up will be the intersection
    res = np.intersect1d(X, X_comp)
    print(f"Result of part 1: {np.prod(res)}")

    # For part 2, we will deal with the combinations
    for a, b, c in combinations(X, 3):
        if a + b + c == 2020:
            res = a * b * c
            break
    print(f"Result of part 2: {res}")


if __name__ == "__main__":
    main()
