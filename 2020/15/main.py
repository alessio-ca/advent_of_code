import time

import numpy as np
from numba import njit  # type: ignore


def python_function(X: np.ndarray, length: int) -> int:
    """Convenience function for the challenge"""
    lookup_list = [0] * length
    # Initialise lookup list
    # Index is the number, value is the last seen
    for i, num in enumerate(X[:-1]):
        lookup_list[num] = i + 1
    # Start with the last number
    last_num = X[-1]
    for i in range(X.shape[0], length):
        if lookup_list[last_num]:
            # If it exists, next num is the interval
            next_num = i - lookup_list[last_num]
        else:
            #  Else, next num is 0
            next_num = 0
        # Update lookup and last_num
        lookup_list[last_num] = i
        last_num = next_num

    return last_num


@njit
def numba_function(X: np.ndarray, length: int) -> int:
    """Same convenience function for the challenge,
    with numba compilation
    """
    lookup_list = [0] * length
    # Initialise lookup list
    # Index is the number, value is the last seen
    for i, num in enumerate(X[:-1]):
        lookup_list[num] = i + 1
    # Start with the last number
    last_num = X[-1]
    for i in range(X.shape[0], length):
        if lookup_list[last_num]:
            # If it exists, next num is the interval
            next_num = i - lookup_list[last_num]
        else:
            #  Else, next num is 0
            next_num = 0
        # Update lookup and last_num
        lookup_list[last_num] = i
        last_num = next_num

    return last_num


def main():
    input_X = np.loadtxt("2020/15/input.txt", delimiter=",", dtype=np.int64)

    length = 2020
    # For part 1, we can brute force it with numpy
    X = [-1] * np.ones(shape=(length,), dtype="int")
    Y = np.arange(length)
    X[: input_X.shape[0]] = input_X
    for i in range(input_X.shape[0], length):
        same = Y[(Y < i) & (X[i - 1] - X == 0)]
        # If the number never appeared,
        if same.shape[0] < 2:
            X[i] = 0
        else:
            X[i] = same[-1] - same[-2]
    print(f"Result of part 1: {X[-1]}")

    # For part 2, this would take too much time.
    # To optimize, we can use a lookup list
    # To further optimize, we can use numba on the lookup list solution :)
    start = time.time()
    result = python_function(input_X, 30000000)
    end = time.time()
    print(f"Result of part 2 (python): {result} ({end - start:.2f}s)")

    start = time.time()
    result = numba_function(input_X, 30000000)
    end = time.time()
    print(f"Result of part 2 (numba): {result} ({end - start:.2f}s)")
    start = time.time()


if __name__ == "__main__":
    main()
