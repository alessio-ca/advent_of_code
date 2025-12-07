import numpy as np

from utils import read_input_batch


def main():
    input_file = read_input_batch("2021/13/input.txt", line_split=False)
    coords = [tuple(map(int, line.split(","))) for line in input_file[0]]
    folds = [
        (1 if axis == "y" else 0, int(value))
        for (axis, value) in [line.split(" ")[-1].split("=") for line in input_file[1]]
    ]

    # Create 2D matrix of coords
    X = np.zeros(
        shape=(max([y for (_, y) in coords]) + 1, max([x for (x, _) in coords])) + 1,
        dtype=int,
    )

    # Set points
    for x, y in coords:
        X[y, x] = 1

    #  Fold
    for i, (axis, value) in enumerate(folds):
        # Define the region interested by the fold as a (2*value + 1)
        #  window centered in value
        slice_start = X.shape[not axis] - 2 * value - 1
        slice_range = slice(slice_start, value)
        slice_fold = slice(value + 1, None)

        # The new slice of X is the lower part of the resulting matrix after folding
        slice_new = slice(None, value)

        if axis == 0:
            # Slice on the horizontal axis & add the LR-flipped fold
            X[:, slice_range] += np.fliplr(X[:, slice_fold])
            X = X[:, slice_new]
        else:
            # Slice on the vertical axis & add the UD-flipped fold
            X[slice_range, :] += np.flipud(X[slice_fold, :])
            X = X[slice_new, :]

        # If first fold, sum the number of dots
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
