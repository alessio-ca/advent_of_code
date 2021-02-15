"""
--- Day 15: Rambunctious Recitation ---

You catch the airport shuttle and try to book a new flight to your vacation island. Due
 to the storm, all direct flights have been cancelled, but a route is available to get
  around the storm. You take it.

While you wait for your flight, you decide to check in with the Elves back at the North
 Pole. They're playing a memory game and are ever so excited to explain the rules!

In this game, the players take turns saying numbers. They begin by taking turns reading
 from a list of starting numbers (your puzzle input). Then, each turn consists of
  considering the most recently spoken number:

If that was the first time the number has been spoken, the current player says 0.
Otherwise, the number had been spoken before; the current player announces how many
 turns apart the number is from when it was previously spoken.
So, after the starting numbers, each turn results in that player speaking aloud either
 0 (if the last number is new) or an age (if the last number is a repeat).

For example, suppose the starting numbers are 0,3,6:

Turn 1: The 1st number spoken is a starting number, 0.
Turn 2: The 2nd number spoken is a starting number, 3.
Turn 3: The 3rd number spoken is a starting number, 6.
Turn 4: Now, consider the last number spoken, 6. Since that was the first time the
 number had been spoken, the 4th number spoken is 0.
Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before,
 the next number to speak is the difference between the turn number when it was last
  spoken (the previous turn, 4) and the turn number of the time it was most recently
   spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5
 and 2. So, the 6th number spoken is 5 - 2, 3.
Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart,
 the 7th number spoken is 1.
Turn 8: Since 1 is new, the 8th number spoken is 0.
Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference
 between them, 4.
Turn 10: 4 is new, so the 10th number spoken is 0.
(The game ends when the Elves get sick of playing or dinner is ready, whichever comes
 first.)

Their question for you is: what will be the 2020th number spoken? In the example above,
 the 2020th number spoken will be 436.

Here are a few more examples:

Given the starting numbers 1,3,2, the 2020th number spoken is 1.
Given the starting numbers 2,1,3, the 2020th number spoken is 10.
Given the starting numbers 1,2,3, the 2020th number spoken is 27.
Given the starting numbers 2,3,1, the 2020th number spoken is 78.
Given the starting numbers 3,2,1, the 2020th number spoken is 438.
Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
Given your starting numbers, what will be the 2020th number spoken?
"""
import numpy as np
import time
from numba import njit


def python_function(X: np.array, length: int) -> int:
    """Convenience function for the challenge"""
    lookup_list = [0] * length
    # Initialise lookup list
    # Index is the number, value is the last seen
    for i, num in enumerate(X[:-1]):
        lookup_list[num] = i + 1
    # Start with the last number
    last_num = X[-1]
    for i in range(X.shape[0], length):
        if lookup_list[last_num]:
            # If it exists, next num is the interval
            next_num = i - lookup_list[last_num]
        else:
            #  Else, next num is 0
            next_num = 0
        # Update lookup and last_num
        lookup_list[last_num] = i
        last_num = next_num

    return last_num


@njit
def numba_function(X: np.array, length: int) -> int:
    """Same convenience function for the challenge,
    with numba compilation
    """
    lookup_list = [0] * length
    # Initialise lookup list
    # Index is the number, value is the last seen
    for i, num in enumerate(X[:-1]):
        lookup_list[num] = i + 1
    # Start with the last number
    last_num = X[-1]
    for i in range(X.shape[0], length):
        if lookup_list[last_num]:
            # If it exists, next num is the interval
            next_num = i - lookup_list[last_num]
        else:
            #  Else, next num is 0
            next_num = 0
        # Update lookup and last_num
        lookup_list[last_num] = i
        last_num = next_num

    return last_num


def main():
    input_X = np.loadtxt("2020/15/input.txt", delimiter=",", dtype=np.int64)

    length = 2020
    # For part 1, we can brute force it with numpy
    X = [-1] * np.ones(shape=(length,), dtype="int")
    Y = np.arange(length)
    X[: input_X.shape[0]] = input_X
    for i in range(input_X.shape[0], length):
        same = Y[(Y < i) & (X[i - 1] - X == 0)]
        # If the number never appeared,
        if same.shape[0] < 2:
            X[i] = 0
        else:
            X[i] = same[-1] - same[-2]
    print(f"Result of part 1: {X[-1]}")

    # For part 2, this would take too much time.
    # To optimize, we can use a lookup list
    # To further optimize, we can use numba on the lookup list solution :)
    start = time.time()
    result = python_function(input_X, 30000000)
    end = time.time()
    print(f"Result of part 2 (python): {result} ({end-start:.2f}s)")

    start = time.time()
    result = numba_function(input_X, 30000000)
    end = time.time()
    print(f"Result of part 2 (numba): {result} ({end-start:.2f}s)")
    start = time.time()


if __name__ == "__main__":
    main()
