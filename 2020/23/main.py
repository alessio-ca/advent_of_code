import numpy as np
from numba import njit  # type: ignore

from utils import read_input


@njit
def do_round(x: np.ndarray, num_round: int):
    # Create pointer array
    # The pointer array always points to the next element in the sequence
    # E.g: pointer[0] = element next to 0 in the sequence
    pointer = np.zeros(shape=x.shape, dtype=np.int64)
    pointer[x] = np.roll(x, -1)
    # Initial index is the first element
    index = x[0]
    for i in range(num_round):
        # Fetch the 3 next cups using pointer
        cup_1 = pointer[index]
        cup_2 = pointer[cup_1]
        cup_3 = pointer[cup_2]
        destination = index - 1
        # Find new destination by looping and take the first result%length not in the
        #  fetched cups
        while destination % x.shape[0] in (cup_1, cup_2, cup_3):
            destination -= 1

        # Assign new positions:
        # The element next to index is now the element next to cup_3
        pointer[index] = pointer[cup_3]
        # The element next to cup_3 is now the element next to destination
        pointer[cup_3] = pointer[destination]
        # The element next to destination is now cup_1
        pointer[destination] = cup_1
        # Finally, the new index is the element next to index
        index = pointer[index]
    return index, pointer


def decode_pointer(pointer: np.ndarray):
    # Decode pointer by obtaining the sequence with 1 at the end
    output_sequence = np.zeros(shape=pointer.shape, dtype="int")
    index = 0
    for i in range(len(output_sequence)):
        output_sequence[i] = pointer[index]
        index = output_sequence[i]

    return output_sequence + 1


def main():
    input_file = read_input("2020/23/input.txt")
    input_sequence = np.array([int(el) for el in input_file[0]], dtype="int")
    # Substract 1 (to enable indexing)
    input_sequence = input_sequence - 1
    # Obtain output index and pointer array
    index, pointer = do_round(input_sequence, 100)
    # Decode pointer array and remove one
    output_sequence = decode_pointer(pointer)
    print(output_sequence)
    result = int("".join([str(x) for x in output_sequence[:-1]]))
    print(f"Result of part 1: {result}")

    input_sequence_long = np.array(
        [
            input_sequence[i] if i < input_sequence.shape[0] else i
            for i in range(1000000)
        ],
        dtype="int",
    )
    index, pointer = do_round(input_sequence_long, 10000000)
    # Fetch the elements next to 0 (remember, we substracted 0 at the start)
    el_1 = pointer[0]
    el_2 = pointer[el_1]
    print(f"Result of part 2: {(el_1 + 1) * (el_2 + 1)}")


if __name__ == "__main__":
    main()
