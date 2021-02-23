"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a password. The
 Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay
 the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these
 criteria?
"""
import numpy as np
from itertools import product
from collections import Counter


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
