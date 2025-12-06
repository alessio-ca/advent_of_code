import numpy as np

from utils import read_input


def main():
    input_file = read_input("2020/05/input.txt")
    data = np.array([list(line) for line in input_file])

    #  Convert to binary array
    data = (data == "B") | (data == "R")
    # For part 1, convert to base 10
    data_int = data.dot(2 ** np.arange(data.T.shape[0])[::-1])
    print(f"Result of part 1: {data_int.max()}")

    #  For part 2, define the set of valid seats and occupied seats
    valid_seats = set(np.arange(data_int.min(), data_int.max()))
    occupied_seats = set(data_int.flatten())
    print(f"Result of part 2: {valid_seats.difference(occupied_seats)}")


if __name__ == "__main__":
    main()
