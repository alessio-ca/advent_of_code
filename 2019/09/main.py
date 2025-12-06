from enum import Enum
from typing import List

import numpy as np


class OpCode(Enum):
    STOP = 99


class InitMode(Enum):
    NORMAL = 0
    REPRISE = 1


class Intcode:
    """Class for IntCode"""

    def __init__(self, instructions: np.ndarray):
        self.orig_instructions = instructions
        # Default input is 0
        self.input = [0]
        self.reset()

    def reset(self):
        self.index = 0
        self.base = 0
        self.is_first_exec = 0
        self.ops = np.zeros(shape=(10000,), dtype=np.int64)
        self.ops[: len(self.orig_instructions)] = self.orig_instructions

    # In normal mode, reset after assigning inputs
    # In reprise mode, only assign inputs
    def init_mode(self, init_mode: InitMode, input_values: List[int]):
        self.input = input_values
        if init_mode == InitMode.NORMAL:
            self.reset()
        elif init_mode == InitMode.REPRISE:
            if self.is_first_exec == 0:
                # Provide full input
                self.input = input_values
            else:
                # Only provide input signal -- pop the setting
                self.input.pop()
        else:
            raise Exception(f"Init Mode {init_mode} not supported")

    def get_params(self, modes, num: int):
        params = []
        for mode, value in zip(modes, range(self.index + 1, self.index + num)):
            if mode == "2":
                params.append(self.ops[value] + self.base)
            elif mode == "1":
                params.append(value)
            elif mode == "0":
                params.append(self.ops[value])
            else:
                raise Exception(f"Mode {mode} is not supported.")

        return params

    def run(self, print_mode=False):
        while True:
            # Fetch instruction -- split in op and modes
            op = self.ops[self.index] % 100
            modes = list(reversed(f"{self.ops[self.index] // 100:03d}"))

            # Stop if stop op is reached or input is OpCode.STOP
            if op == 99:
                return OpCode.STOP

            # Execute instructions
            if op == 1:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = self.ops[values[0]] + self.ops[values[1]]
                self.index += 4
            elif op == 2:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = self.ops[values[0]] * self.ops[values[1]]
                self.index += 4
            elif op == 3:
                values = self.get_params(modes, 2)
                self.ops[values[0]] = self.input.pop()
                self.index += 2
            elif op == 4:
                values = self.get_params(modes, 2)
                # Update is_first_run status
                self.is_first_exec = 1
                self.index += 2

                if print_mode:
                    print(self.ops[values[0]])
                else:
                    return self.ops[values[0]]

            elif op == 5:
                values = self.get_params(modes, 3)
                if self.ops[values[0]] != 0:
                    self.index = self.ops[values[1]]
                else:
                    self.index += 3
            elif op == 6:
                values = self.get_params(modes, 3)
                if self.ops[values[0]] == 0:
                    self.index = self.ops[values[1]]
                else:
                    self.index += 3
            elif op == 7:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = (
                    1 if self.ops[values[0]] < self.ops[values[1]] else 0
                )
                self.index += 4
            elif op == 8:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = (
                    1 if self.ops[values[0]] == self.ops[values[1]] else 0
                )
                self.index += 4
            elif op == 9:
                values = self.get_params(modes, 2)
                self.base += self.ops[values[0]]
                self.index += 2

            else:
                return -1


def main():
    input_array = np.loadtxt("2019/09/input.txt", delimiter=",", dtype=np.int64)
    instructions = input_array.copy()

    # Init intcode & initialize in normal mode
    intcode = Intcode(instructions)

    intcode.init_mode(InitMode.NORMAL, [1])
    # Run
    out = intcode.run()
    print(f"Result of part 1: {out}")

    intcode.init_mode(InitMode.NORMAL, [2])
    # Run
    out = intcode.run()
    print(f"Result of part 2: {out}")


if __name__ == "__main__":
    main()
