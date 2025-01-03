from utils import read_input, timefunc
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def mix(values: np.ndarray, numbers: np.ndarray) -> np.ndarray:
    return values ^ numbers


def prune(numbers: np.ndarray) -> np.ndarray:
    # Modulo is equivalent to bitshift
    return numbers & ((1 << 24) - 1)


def sequence(numbers: np.ndarray, n: int) -> np.ndarray:
    X = numbers.copy()
    Y = np.zeros(shape=(n, len(numbers)), dtype=int)
    for i in range(n):
        X = prune(mix(X << 6, X))
        X = prune(mix(X >> 5, X))
        X = prune(mix(X << 11, X))
        Y[i, :] = X

    return Y


def highest_price(numbers: np.ndarray, n: int) -> int:
    # Create sequence of numbers, modulo 10 (last digit)
    prices = sequence(numbers, n) % 10
    # Calculate diff by row and shift by 10
    # (to generate values in the [0...19] range)
    diffs = np.diff(prices, axis=0) + 10
    # Obtain 4-sized rolling windows and encode each window using base 19
    windows = (
        sliding_window_view(diffs + 10, axis=0, window_shape=4)
        * 19 ** np.arange(4)[::-1]
    ).sum(-1)
    # Create empty array of bananas
    bananas = np.zeros(shape=(windows.max() + 1,), dtype=int)
    for i in np.arange(windows.shape[1]):
        # For each buyer, obtain the windows idx (as base19 encoded)
        # and the idx to retrieve the prices corresponding to the first appearance
        # of that window
        window_idx, price_idx = np.unique(windows[:, i], return_index=True)
        # Update the bananas array: each window is update with the associated price
        bananas[window_idx] += prices[price_idx + 4, i]

    return bananas.max()


@timefunc
def main(filename: str):
    numbers = np.array(list(map(int, read_input(filename))), dtype=int)
    print(f"Result of part 1: {sequence(numbers, 2000)[-1, :].sum()}")
    print(f"Result of part 2: {highest_price(numbers, 2000)}")


if __name__ == "__main__":
    main("2024/22/input.txt")
