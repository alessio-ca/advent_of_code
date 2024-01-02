import numpy as np
from utils import read_input


def perform_part_1(X: np.ndarray) -> np.ndarray:
    X_out = np.zeros(shape=X.shape, dtype=np.int64)

    for iy, ix in np.ndindex(X.shape):
        # Check if edge
        if (ix == 0) | (ix == X.shape[0] - 1) | (iy == 0) | (iy == X.shape[1] - 1):
            X_out[ix, iy] = 1
        else:
            # Create directional arrays
            array_l, array_r = X[:ix, iy], X[(ix + 1) :, iy]
            array_u, array_d = X[ix, :iy], X[ix, (iy + 1) :]
            # Calculate max elements
            max_array = [arr.max() for arr in [array_l, array_r, array_u, array_d]]
            # Check if there is any direction whose max is lower than the element
            X_out[ix, iy] = min(max_array) < X[ix, iy]

    return X_out


def perform_part_2(X: np.ndarray) -> np.ndarray:
    X_out = np.ones(shape=X.shape, dtype=np.int64)

    for iy, ix in np.ndindex(X.shape):
        # Check if edge
        if (ix == 0) | (ix == X.shape[0] - 1) | (iy == 0) | (iy == X.shape[1] - 1):
            X_out[ix, iy] = 0
        else:
            el = X[ix, iy]
            # Create directional arrays
            array_l, array_r = X[:ix, iy] >= el, X[(ix + 1) :, iy] >= el
            array_u, array_d = X[ix, :iy] >= el, X[ix, (iy + 1) :] >= el
            # Calculate number of visible trees
            for arr in [np.flip(array_l), array_r, np.flip(array_u), array_d]:
                # If we get to the edge, consider the shape
                if arr.sum() == 0:
                    X_out[ix, iy] *= arr.shape[0]
                # Otherwise, consider the first index + 1
                else:
                    X_out[ix, iy] *= np.argmax(arr) + 1

    return X_out


def main(filename: str):
    X_raw = read_input(filename, line_strip=True)
    X = np.array([[int(i) for i in row] for row in X_raw], dtype=np.int64)

    X_out = perform_part_1(X)
    print(f"Result of part 1: {X_out.sum()}")

    X_out = perform_part_2(X)
    print(f"Result of part 2: {X_out.max()}")


if __name__ == "__main__":
    main("2022/08/input.txt")
