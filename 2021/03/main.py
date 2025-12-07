import collections
from typing import List

from utils import read_input


def rec_fun(x: List[str], mode: str, y: int = 0) -> str:
    """Simple recursive function to perform candidate selection"""
    try:
        # Sort each string by value & key in ascending order (this will break ties
        #  according to the rule specified in the problem description)
        candidates = sorted(
            collections.Counter([z[y] for z in x]).most_common(),
            key=lambda x: (x[1], x[0]),
            reverse=True,
        )
        # Depending on the selected mode, select the appropriate candidate
        if mode == "most":
            bit_filter = candidates[0][0]
        elif mode == "least":
            bit_filter = candidates[-1][0]
        else:
            raise ValueError
        # Filter list of binary strings
        x = list(filter(lambda z: z[y] == bit_filter, x))
        # Apply recursive call
        return rec_fun(x, mode=mode, y=y + 1)

    # If we navigated all the bits, return the last surviving element
    except IndexError:
        return x[-1]


def main():
    input_file = read_input("2021/03/input.txt")
    # Obtain gamma and epsilon rate
    gamma_rate = [
        collections.Counter([x[i] for x in input_file]).most_common(1)[0][0]
        for i in range(len(input_file[0]))
    ]
    epsilon_rate = ["0" if x == "1" else "1" for x in gamma_rate]
    # Convert to decimal
    gamma_rate = int("".join(gamma_rate), 2)
    epsilon_rate = int("".join(epsilon_rate), 2)
    print(f"Result of part 1: {gamma_rate * epsilon_rate}")

    # Obtain oxygen and co2 scrubber ratings
    oxygen_rate = rec_fun(input_file, "most")
    scrubber_rate = rec_fun(input_file, "least")
    # Convert to decimal
    oxygen_rate = int("".join(oxygen_rate), 2)
    scrubber_rate = int("".join(scrubber_rate), 2)
    print(f"Result of part 2: {oxygen_rate * scrubber_rate}")


if __name__ == "__main__":
    main()
