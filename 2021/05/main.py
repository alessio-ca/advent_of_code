import numpy as np

from utils import read_input


def populate_matrix(
    p1: np.ndarray, p2: np.ndarray, diagonal: bool = False
) -> np.ndarray:
    # Create empty matrix
    X = np.zeros(
        shape=(
            max(p1[:, 1].max() + 1, p2[:, 1].max() + 1),
            max(p1[:, 0].max() + 1, p2[:, 0].max() + 1),
        )
    )
    # Loop over points
    for pp1, pp2 in zip(p1, p2):
        min_x, max_x = min(pp1[1], pp2[1]), max(pp1[1], pp2[1])
        min_y, max_y = min(pp1[0], pp2[0]), max(pp1[0], pp2[0])

        # If horiz or vertical line, simply add one to all points on the line
        if (min_x == max_x) | (min_y == max_y):
            X[min_x : max_x + 1, min_y : max_y + 1] += 1

        # If diagonal, generate points on the diagonal line
        else:
            if diagonal:
                # Create view of the area where the diagonal lives
                X_temp = X[min_x : max_x + 1, min_y : max_y + 1]
                # Create a identity matrix mask
                mask = np.eye(len(X_temp), dtype=bool)
                # Flip the mask depending on the points arrangement
                if (pp2[0] < pp1[0]) != (pp2[1] < pp1[1]):
                    mask = np.fliplr(mask)
                # Add oone to the points on the line
                X_temp[mask] += 1
            else:
                pass
    return X


def main():
    input_file = read_input("2021/05/input.txt")
    p1 = []
    p2 = []
    for line in input_file:
        p1.append(list(map(int, line.split(" ")[0].split(","))))
        p2.append(list(map(int, line.split(" ")[2].split(","))))

    p1 = np.array(p1)
    p2 = np.array(p2)

    # For part 1, diagonals are disabled by default
    X = populate_matrix(p1, p2)
    print(f"Result of part 1: {(X > 1).sum()}")

    # For part 2, diagonals are enabled
    X = populate_matrix(p1, p2, diagonal=True)
    print(f"Result of part 2: {(X > 1).sum()}")


if __name__ == "__main__":
    main()
