import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def main():
    X = np.loadtxt("2021/01/input.txt", dtype=int)
    # Calculate the array of differences
    X_diff = np.diff(X)
    # Find the number of positives
    res_1 = (X_diff > 0).sum()
    print(f"Result of part 1: {res_1}")
    # For Part 2, we create a sliding window of size 3 and take the sum along the second
    #  axis (columns)
    Y = sliding_window_view(X, 3).sum(axis=1)
    # Calculate the array of differences
    Y_diff = np.diff(Y)
    # Find the number of positives
    res_2 = (Y_diff > 0).sum()
    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main()
