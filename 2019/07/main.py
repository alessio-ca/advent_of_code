import math
from enum import Enum
from itertools import permutations
from typing import List

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
        self.is_first_exec = 0
        self.ops = self.orig_instructions.copy()

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
        return [
            value if mode == "1" else self.ops[value]
            for mode, value in zip(modes, range(self.index + 1, self.index + num))
        ]

    def run(self):
        while True:
            # Fetch instruction -- split in op and modes
            op = OpCode(self.ops[self.index] % 100)
            modes = reversed(f"{self.ops[self.index] // 100:03d}")

            # Stop if stop op is reached or input is OpCode.STOP
            if op is OpCode.STOP:
                return OpCode.STOP

            # Execute instructions
            if op is OpCode.ADD:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = self.ops[values[0]] + self.ops[values[1]]
                self.index += 4
            elif op is OpCode.MUL:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = self.ops[values[0]] * self.ops[values[1]]
                self.index += 4
            elif op is OpCode.TAKE:
                values = self.get_params(modes, 2)
                self.ops[values[0]] = self.input.pop()
                self.index += 2
            elif op is OpCode.GIVE:
                values = self.get_params(modes, 2)
                # Update is_first_run status
                self.is_first_exec = 1
                self.index += 2
                return self.ops[values[0]]
            elif op is OpCode.JUMP_TRUE:
                values = self.get_params(modes, 3)
                if self.ops[values[0]] != 0:
                    self.index = self.ops[values[1]]
                else:
                    self.index += 3
            elif op is OpCode.JUMP_FALSE:
                values = self.get_params(modes, 3)
                if self.ops[values[0]] == 0:
                    self.index = self.ops[values[1]]
                else:
                    self.index += 3
            elif op is OpCode.LT:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = (
                    1 if self.ops[values[0]] < self.ops[values[1]] else 0
                )
                self.index += 4
            elif op is OpCode.EQ:
                values = self.get_params(modes, 4)
                self.ops[values[2]] = (
                    1 if self.ops[values[0]] == self.ops[values[1]] else 0
                )
                self.index += 4
            else:
                return -1


def main():
    input_array = np.loadtxt("2019/07/input.txt", delimiter=",", dtype=np.int64)
    instructions = input_array.copy()

    # Init intcode & set max signal to -inf
    intcode = Intcode(instructions)
    max_signal = -math.inf

    for settings in permutations("01234"):
        # First signal is always 0
        signal = 0
        # Loop over the amplifier
        for i in range(5):
            # Init in Normal mode and run
            intcode.init_mode(InitMode.NORMAL, [signal, settings[i]])
            signal = intcode.run()

        max_signal = max(max_signal, signal)

    print(f"Result of part 1: {max_signal}")

    # Define list of amplifiers
    amplifiers = [Intcode(instructions) for _ in range(5)]
    for settings in permutations("56789"):
        # Reset the amplifiers
        for i in range(5):
            amplifiers[i].reset()
        # First signal is always 0
        signal = 0
        output_signal = 0
        # Run in feedbackmode until OpMode.STOP is detected
        while signal is not OpCode.STOP:
            # Loop over the amplifiers
            for i in range(5):
                # Update the signal on the amplifier in reprise mode
                amplifiers[i].init_mode(InitMode.REPRISE, [signal, settings[i]])
                # Run
                signal = amplifiers[i].run()

            # Record output signal only if last amplifier did not halt
            output_signal = signal if signal is not OpCode.STOP else output_signal

        max_signal = max(max_signal, output_signal)

    print(f"Result of part 2: {max_signal}")


if __name__ == "__main__":
    main()
