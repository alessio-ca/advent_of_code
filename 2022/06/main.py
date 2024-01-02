import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def subroutine(input: np.ndarray, num_chars: int) -> int:
    # Create sliding window of size `num_chars`
    # It generates an array where each row is a window
    X = sliding_window_view(input, num_chars)
    # Iterate over rows and search for the first row with `num_chars` unique elements
    for i, row in enumerate(X):
        if len(set(row)) == num_chars:
            break
    return i + num_chars


def main(filename: str):
    with open(filename) as f:
        X_raw = np.array(list(f.read()), dtype="<U3")

    print(f"Result of part 1: {subroutine(X_raw, 4)}")
    print(f"Result of part 2: {subroutine(X_raw, 14)}")


if __name__ == "__main__":
    main("2022/06/input.txt")
