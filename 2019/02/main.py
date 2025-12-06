from itertools import product

import numpy as np

OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_STOP = 99


# Note: this function can run much faster with the @njit decorator from numba!
def program_loop(X: np.ndarray):
    # Make copy
    X = X.copy()

    # Start with index 0
    index = 0
    while X[index] != OPCODE_STOP:
        # Perform program instructions
        if X[index] == OPCODE_ADD:
            X[X[index + 3]] = X[X[index + 2]] + X[X[index + 1]]
        elif X[index] == OPCODE_MUL:
            X[X[index + 3]] = X[X[index + 2]] * X[X[index + 1]]
        else:
            return -1
        index += 4

    return X[0]


def main():
    input_array = np.loadtxt("2019/02/input.txt", delimiter=",", dtype=np.int64)
    program = input_array.copy()
    program[1] = 12
    program[2] = 2

    print(f"Result of part 1: {program_loop(program)}")

    # Loop over combinations of verb and noun
    for verb, noun in product(range(100), repeat=2):
        program[1] = verb
        program[2] = noun
        result = program_loop(program)
        if result == 19690720:
            break

    print(f"Result of part 2: {100 * verb + noun}")


if __name__ == "__main__":
    main()
