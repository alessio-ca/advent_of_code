from utils import read_input
from scipy.signal import convolve2d

import numpy as np
CONV_FILTER = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int32)

def rolls_to_remove(X: np.ndarray) -> np.ndarray:
    Y = convolve2d(X, CONV_FILTER, mode="same", boundary="fill", fillvalue=0)
    rolls_to_remove = (Y < 4) & (X == 1)
    return rolls_to_remove

def main(filename: str):
    data = read_input(filename)
    # Create numpy array of the initial grid and initialize system
    X = np.array([
        list(map(lambda x: 1 if x == '@' else 0, row))
        for row in data
    ], dtype=np.int32)

    to_remove = rolls_to_remove(X)
    res_1 = to_remove.sum()
    print(f"Result of part 1: {res_1}")
    res_2 = 0
    while to_remove.sum() > 0:
        X[to_remove] = 0
        to_remove = rolls_to_remove(X)
        res_2+= to_remove.sum()
    print(f"Result of part 2: {res_1 + res_2}")

if __name__ == "__main__":
    main("2025/04/input.txt")
