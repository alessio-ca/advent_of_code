import numpy as np

from utils import read_input

TREE = "#"
SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def main():
    input_file = read_input("2020/03/input.txt")
    data = np.array([list(line) for line in input_file])
    height, width = data.shape

    # Define tree array
    tree_count = np.zeros(shape=(len(SLOPES),), dtype="int")

    for i, (right, down) in enumerate(SLOPES):
        # Get range array of the number of possible y positions
        y_index = np.arange(height / down).astype(int)
        # Define sequence of (x,y) depending on slope and y_index
        y = y_index * down
        x = y_index * right
        # The x position is periodic
        x %= width
        # Count trees
        tree_count[i] = (data[y, x] == TREE).sum()

    print(f"Result of part 1: {tree_count[1]}")
    print(f"Result of part 2: {np.prod(tree_count)}")


if __name__ == "__main__":
    main()
