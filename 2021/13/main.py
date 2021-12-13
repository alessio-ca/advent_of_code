from utils import read_input_batch
import numpy as np


def main():
    input_file = read_input_batch("2021/13/input.txt", line_split=False)
    coords = [tuple(map(int, line.split(","))) for line in input_file[0]]
    folds = [
        (1 if axis == "y" else 0, int(value))
        for (axis, value) in [line.split(" ")[-1].split("=") for line in input_file[1]]
    ]

    # Create 2D matrix of coords
    X = np.zeros(
        shape=(max([y for (_, y) in coords]) + 1, max([x for (x, _) in coords]) + 1),
        dtype=int,
    )

    # Set points
    for x, y in coords:
        X[y, x] = 1

    #  Fold
    for i, (axis, value) in enumerate(folds):
        if axis == 0:
            slice_start = X.shape[1] - 2 * value - 1
            X[:, slice_start:value] += np.fliplr(X[:, value + 1 :])
            X = X[:, :value]
        else:
            slice_start = X.shape[0] - 2 * value - 1
            X[slice_start:value, :] += np.flipud(X[value + 1 :, :])
            X = X[:value, :]
        # First fold
        if i == 0:
            # Sum on axis
            res_1 = (X > 0).sum()

    # Get final image
    encoded = X > 0
    map_to_pixel = {0: " ", 1: "#"}
    decoded = ""
    for row in encoded:
        decoded += "".join(map(map_to_pixel.get, row)) + "\n"

    print(f"Result of part 1: {res_1}")
    print("Result of part 2: ")
    print("")
    print(f"{decoded}")


if __name__ == "__main__":
    main()
