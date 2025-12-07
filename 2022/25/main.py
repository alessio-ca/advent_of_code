from utils import read_input

SNAFU_DICT = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def number_to_base(n: int, base: int) -> list[int]:
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % base))
        n //= base
    return digits[::-1]


def quinary_to_balanced(quinary: list[int]) -> str:
    quinary.reverse()
    c = 0
    balanced: list[int] = []
    for digit in quinary:
        digit += c
        c = digit // 3
        balanced.append(digit % 3 - 2 * c)

    balanced.reverse()
    snafu_reverse = {value: key for key, value in SNAFU_DICT.items()}
    balanced_to_str: list[str] = [snafu_reverse[digit] for digit in balanced]
    return "".join(balanced_to_str)


def main(filename: str):
    snafu_numbers = [[SNAFU_DICT[c] for c in line] for line in read_input(filename)]
    dec_number = sum(
        sum(5**i * d for i, d in enumerate(number[::-1])) for number in snafu_numbers
    )
    # Obtain list representation by power of 5
    quin_list = number_to_base(dec_number, 5)
    print(f"Result of part 1: {quinary_to_balanced(quin_list)}")


if __name__ == "__main__":
    main("2022/25/input.txt")
