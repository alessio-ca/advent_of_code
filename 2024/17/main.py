from utils import read_input_batch
import re
from collections import deque
import heapq


class Program:
    def __init__(self, filename: str):
        registers, program = read_input_batch(filename, line_split=False)
        self.A, self.B, self.C = list(
            map(lambda x: int(re.findall(r"\d+", x)[0]), registers)
        )
        self.program = list(map(int, re.findall(r"\d+", program[0])))
        self.pointer = 0
        self.out = deque([])
        self.stack = deque([])

    def instruction(self, i: int, o: int):
        if i == 0:
            self.A //= 2 ** self.combo(o)
        elif i == 1:
            self.B ^= o
        elif i == 2:
            self.B = self.combo(o) % 8
        elif i == 3:
            # Point to o-2 to correct for
            # the constant +2 increase
            if self.A != 0:
                self.pointer = o - 2
        elif i == 4:
            self.B ^= self.C
        elif i == 5:
            self.out.append(self.combo(o) % 8)
        elif i == 6:
            self.B = self.A // 2 ** self.combo(o)
        elif i == 7:
            self.C = self.A // 2 ** self.combo(o)

        self.pointer += 2

    def combo(self, i: int):
        if i <= 3:
            return i
        elif i == 4:
            return self.A
        elif i == 5:
            return self.B
        elif i == 6:
            return self.C
        else:
            raise ValueError(f"You should NOT have combo for {i}")

    def run(self):
        while self.pointer < len(self.program) - 1:
            self.instruction(self.program[self.pointer], self.program[self.pointer + 1])


def op(A: int, is_test: bool) -> int:
    if is_test:
        # For the example, the program performs the following op
        A = A >> 3
        return A % 8
    else:
        # For the input, adapt to whatever the input does!
        B = (A % 8) ^ 1
        C = A >> B
        return (B ^ C ^ 4) % 8


def reverse_iteration(targets, is_test: bool = True) -> int:
    """The programs for part 2 can be represented in condensed form as a loop:
    out = []
    while A > 0:
        out.append(op(A)) (operation producing an output based only on A)
        A = A >> 3  (right-shift A by 3 == divide&floor by 2**3)
    Find the smallest A for which out == targets.
    Use a heap to keep track of valid candidates, and walk
    the `targets` list backward.
    """
    # Structure heap as (A, target_idx)
    # We start from 0 (the final A) and target the last output (1)
    heap = [(0, 1)]
    heapq.heapify(heap)
    while heap:
        # Pop the smallest A ending one op
        # with out = targets[-i]
        end_A, i = heapq.heappop(heap)
        if i > len(targets):
            # We reached the smallest A
            # that produces all the targets
            return end_A

        # Left-Shift end_A by 3 digits
        min_A = end_A << 3
        # Candidate A for target
        # is in the range [A, A+8)
        # (so that A >> 3 produces the same output end_A)
        for A in range(min_A, min_A + 8):
            # If the op produces the target,
            # add A to heap and point to next target
            if op(A, is_test) == targets[-i]:
                heapq.heappush(heap, (A, i + 1))


def main(filename: str):
    input_str = filename.split("/")[-1]
    if "example" in input_str:
        is_test = True
    else:
        is_test = False
    program = Program(filename)
    program.run()
    print(f"Result of part 1: {','.join(list(map(str, program.out)))}")
    print(f"Result of part 2: {reverse_iteration(program.program, is_test=is_test)}")


if __name__ == "__main__":
    main("2024/17/input.txt")
