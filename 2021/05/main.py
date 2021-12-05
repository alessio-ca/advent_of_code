from utils import read_input
import numpy as np


def main():
    input_file = read_input("2021/05/input.txt")
    p1 = []
    p2 = []
    for line in input_file:
        p1.append(list(map(int, line.split(" ")[0].split(","))))
        p2.append(list(map(int, line.split(" ")[2].split(","))))

    p1_orig = np.array(p1)
    p2_orig = np.array(p2)

    # For part 1, filter horizontal & vertical lines
    mask_line = (p1_orig[:, 0] == p2_orig[:, 0]) | (p1_orig[:, 1] == p2_orig[:, 1])
    p1 = p1_orig[mask_line].copy()
    p2 = p2_orig[mask_line].copy()

    X = np.zeros(
        shape=(
            max(p1[:, 1].max() + 1, p2[:, 1].max() + 1),
            max(p1[:, 0].max() + 1, p2[:, 0].max() + 1),
        )
    )
    for pp1, pp2 in zip(p1, p2):
        min_x, max_x = min(pp1[1], pp2[1]), max(pp1[1], pp2[1])
        min_y, max_y = min(pp1[0], pp2[0]), max(pp1[0], pp2[0])
        X[min_x : max_x + 1, min_y : max_y + 1] += 1

    print(f"Result of part 1: {(X>1).sum()}")

    # For part 2, do not filter
    p1 = p1_orig.copy()
    p2 = p2_orig.copy()

    X = np.zeros(
        shape=(
            max(p1[:, 1].max() + 1, p2[:, 1].max() + 1),
            max(p1[:, 0].max() + 1, p2[:, 0].max() + 1),
        )
    )
    for pp1, pp2 in zip(p1, p2):
        min_x, max_x = min(pp1[1], pp2[1]), max(pp1[1], pp2[1])
        min_y, max_y = min(pp1[0], pp2[0]), max(pp1[0], pp2[0])
        # If horiz or vertical line, simply add
        if (min_x == max_x) | (min_y == max_y):
            X[min_x : max_x + 1, min_y : max_y + 1] += 1
        # If diagonal, generate points
        else:
            X_temp = X[min_x : max_x + 1, min_y : max_y + 1]
            mask = np.eye(len(X_temp), dtype=bool)
            if (pp2[0] < pp1[0]) != (pp2[1] < pp1[1]):
                mask = np.fliplr(mask)

            X_temp[mask] += 1

    print(f"Result of part 2: {(X>1).sum()}")


if __name__ == "__main__":
    main()
