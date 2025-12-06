from enum import Enum

import numpy as np


class OpCode(Enum):
    ADD = 1
    MUL = 2
    TAKE = 3
    GIVE = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LT = 7
    EQ = 8
    STOP = 99


def transform_in_digits(n: int, base_array: np.ndarray):
    """Convenience function to transform a number into its digits,
    given by base array"""
    return n // 10**base_array % 10


class Instruction:
    """Class for Instruction"""

    def __init__(self, code: int, base_array: np.ndarray):
        self.code = transform_in_digits(code, base_array)
        # Transform into an opcode -- using first digit (units) and second (tens)
        self.op = OpCode(self.code[-1] + 10 * self.code[-2])
        # Mode should be read right to left
        self.mode = np.flip(self.code[:-2])


class Intcode:
    """Class for IntCode"""

    def __init__(self, instructions: np.ndarray, input_value: int):
        self.orig_instructions = instructions
        # Base array is 10^x, flipped (so that leading zeros are on the left)
        self.base_array = np.flip(np.arange(5))
        # Here, we assign the input statically --
        #  can be replaced by a user prompt in OPCODE TAKE section
        self.input = input_value
        self.reset()

    def reset(self):
        self.index = 0
        self.ops = self.orig_instructions.copy()
        print(f"Input value is {self.input}")

    def run(self):
        while True:
            # Fetch instruction
            instruction = Instruction(self.ops[self.index], self.base_array)
            # Stop if stop op is reached
            if instruction.op is OpCode.STOP:
                return 0

            # Obtain param values according to mode
            values = [
                self.index + (i + 1)
                if instruction.mode[i] == 1
                else self.ops[self.index + (i + 1)]
                for i in range(len(instruction.mode))
            ]

            # Execute instructions
            if instruction.op is OpCode.ADD:
                first, second = self.ops[values[:2]]
                self.ops[values[2]] = first + second
                self.index += 4
            elif instruction.op is OpCode.MUL:
                first, second = self.ops[values[:2]]
                self.ops[values[2]] = first * second
                self.index += 4
            elif instruction.op is OpCode.TAKE:
                self.ops[values[0]] = self.input
                self.index += 2
            elif instruction.op is OpCode.GIVE:
                print(self.ops[values[0]])
                self.index += 2
            elif instruction.op is OpCode.JUMP_TRUE:
                if self.ops[values[0]] != 0:
                    self.index = self.ops[values[1]]
                else:
                    self.index += 3
            elif instruction.op is OpCode.JUMP_FALSE:
                if self.ops[values[0]] == 0:
                    self.index = self.ops[values[1]]
                else:
                    self.index += 3
            elif instruction.op is OpCode.LT:
                self.ops[values[2]] = (
                    1 if self.ops[values[0]] < self.ops[values[1]] else 0
                )
                self.index += 4
            elif instruction.op is OpCode.EQ:
                self.ops[values[2]] = (
                    1 if self.ops[values[0]] == self.ops[values[1]] else 0
                )
                self.index += 4
            else:
                return -1


def main():
    input_array = np.loadtxt("2019/05/input.txt", delimiter=",", dtype=np.int64)
    instructions = input_array.copy()

    print("Part 1:")
    intcode = Intcode(instructions, input_value=1)
    intcode.run()
    print("")

    print("Part 2:")
    intcode.input = 5
    intcode.reset()
    intcode.run()


if __name__ == "__main__":
    main()
