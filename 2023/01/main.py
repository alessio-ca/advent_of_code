from utils import read_input
import re

DIGITS_DICT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0",
}


def convert_literal_to_digit(s: str) -> str:
    """Convert a literal number (e.g. "nine") to a digit (e.g. "9").
    If already a digit, pass."""
    if s in DIGITS_DICT.keys():
        return DIGITS_DICT[s]
    else:
        return s


def main():
    X_raw = read_input("2023/01/input.txt")
    # Extract digits
    digits = [re.findall(r"\d", line) for line in X_raw]
    # Take first and last, concatenate
    numbers = [int(line[0] + line[-1]) for line in digits]
    print(f"Result of part 1: {sum(numbers)}")

    # Extract digits
    digits_pattern = r"(?=(\d|" + r"|".join(DIGITS_DICT.keys()) + r"))"
    raw_digits = [re.findall(digits_pattern, line) for line in X_raw]
    # Convert literal to numbers
    digits = [
        [convert_literal_to_digit(s) for s in line] for line in raw_digits
    ]  # noqa: E501
    # Take first and last, concatenate
    numbers = [int(line[0] + line[-1]) for line in digits]
    print(f"Result of part 2: {sum(numbers)}")


if __name__ == "__main__":
    main()
