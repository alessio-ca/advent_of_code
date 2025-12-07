from typing import Dict, List, Set

from utils import read_input


def _inverse_digit_mapping(
    candidate: Set[str], digits_dict: Dict[int, Set[str]]
) -> int:
    """Perform inverse mapping over a dictionary"""
    for key, value in digits_dict.items():
        if value == candidate:
            return key
    return -1


def find_number(line: List[str], digit: List[str]) -> int:
    """Find the number given the signal line and digit list"""
    # Convert signal lines to sets
    line_set = [set(signal) for signal in line]
    # Compute the length of each signal
    length = list(map(len, line_set))

    digits_dict = {}
    # Assign easy digits
    digits_dict[1] = [i for (i, j) in zip(line_set, length) if j == 2][0]
    digits_dict[4] = [i for (i, j) in zip(line_set, length) if j == 4][0]
    digits_dict[7] = [i for (i, j) in zip(line_set, length) if j == 3][0]
    digits_dict[8] = [i for (i, j) in zip(line_set, length) if j == 7][0]

    # Obtain first segments definition
    #  We use the following number convention:
    #   aaaa
    #  b    c
    #  b    c
    #   dddd
    #  e    f
    #  e    f
    #   gggg
    a = digits_dict[7] - digits_dict[1]
    bd = digits_dict[4] - digits_dict[1]
    eg = digits_dict[8] - (digits_dict[4].union(digits_dict[7]))

    # Obtain 6 letters digits intersections with eight
    six_letters = set().union(
        *[digits_dict[8] - i for (i, j) in zip(line_set, length) if j == 6]
    )

    # Use logic to obtain all other segment definitions
    c = six_letters - (bd.union(eg))
    f = digits_dict[8] - set().union(*[a, bd, c, eg])
    e = six_letters.intersection(eg)
    d = six_letters.intersection(bd)
    b = bd - d

    # Complete the digit dictionary
    digits_dict[0] = digits_dict[8] - d
    digits_dict[2] = digits_dict[8] - b - f
    digits_dict[3] = digits_dict[8] - b - e
    digits_dict[5] = digits_dict[8] - c - e
    digits_dict[6] = digits_dict[8] - c
    digits_dict[9] = digits_dict[8] - e

    # Map digits to the digit dictionary and return the resulting number
    number_digit = int(
        "".join(
            map(
                str,
                [_inverse_digit_mapping(set(number), digits_dict) for number in digit],
            )
        )
    )
    return number_digit


def main():
    input_file = read_input("2021/08/input.txt")
    signals = []
    digits = []
    for line in input_file:
        signals.append(line.split(" | ")[0].split(" "))
        digits.append(line.split(" | ")[1].split(" "))

    # For Part 1, just find digits 2, 4, 3 or 7 long
    res_1 = sum(
        sum(len(number) in [2, 4, 3, 7] for number in entry) for entry in digits
    )
    print(f"Result of part 1: {res_1}")

    # For Part 2, we need to find the correct numbers
    total_sum = 0
    for line, digit in zip(signals, digits):
        # Obtain number
        num = find_number(line, digit)
        total_sum += num

    print(f"Result of part 2: {total_sum}")


if __name__ == "__main__":
    main()
