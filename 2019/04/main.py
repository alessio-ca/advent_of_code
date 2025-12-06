from collections import Counter
from itertools import product

import numpy as np


def main():
    range_min, range_max = np.loadtxt(
        "2019/04/input.txt", delimiter="-", dtype=np.int64
    )
    # Generate all possible combinations -- 0 and 1 can't be there!
    # Remove entries that don't have double digits or are not in the correct order
    gen_passwords = (
        password
        for password in product("23456789", repeat=6)
        if (len(set(password)) < len(password)) and (sorted(password) == list(password))
    )
    # Remove entries not in range from generated passwords
    passwords = [
        password
        for password in map(lambda x: int("".join(str(c) for c in x)), gen_passwords)
        if (password >= range_min) and (password <= range_max)
    ]
    print(f"Result of part 1: {len(passwords)}")

    # Get dictionary of counts in list
    dict_count = map(
        dict,
        map(Counter, ((c for c in str(password)) for password in passwords)),
    )
    # Enforce the last condition
    num_valid_passwords = sum((1 for counter in dict_count if 2 in counter.values()))
    print(f"Result of part 2: {num_valid_passwords}")


if __name__ == "__main__":
    main()
