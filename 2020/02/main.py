import re

from utils import read_input


def main():
    input_file = read_input("2020/02/input.txt")
    # Restructure input
    input_tuples = [
        re.match(r"(\d+)-(\d+) (\w): (\w+)", line).groups() for line in input_file
    ]

    #  For part 1, Create boolean mask of valid passwords
    valid_mask = [
        int(lcount) <= passw.count(char) <= int(hcount)
        for (lcount, hcount, char, passw) in input_tuples
    ]
    print(f"Result of part 1: {sum(valid_mask)}")

    # For part 2, Create boolean mask of valid passwords
    valid_mask = [
        (passw[int(lcount) - 1] == char) != (passw[int(hcount) - 1] == char)
        for (lcount, hcount, char, passw) in input_tuples
    ]
    print(f"Result of part 2: {sum(valid_mask)}")


if __name__ == "__main__":
    main()
