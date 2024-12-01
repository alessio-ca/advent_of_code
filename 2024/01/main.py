import numpy as np
from collections import Counter


def main(filename: str):
    X = np.loadtxt(filename, dtype=int)
    Y = np.diff(np.vstack((np.sort(X[:, 0]), np.sort(X[:, 1]))).T, axis=-1)
    print(f"Result of part 1: {np.abs(Y).sum()}")

    count = Counter(X[:, 1])
    Z = [x * count[x] for x in X[:, 0]]
    print(f"Result of part 2: {sum(Z)}")


if __name__ == "__main__":
    main("2024/01/input.txt")
