"""
--- Day 9: Sensor Boost ---

You've just said goodbye to the rebooted rover and left Mars when you receive a faint
 distress signal coming from the asteroid belt. It must be the Ceres monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The Elves send up
 the latest BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors, for tenuous safety
 reasons, it refuses to do so until the computer it runs on passes some checks to
  demonstrate it is a complete Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support for
 parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in position
 mode: the parameter is interpreted as a position. Like position mode, parameters in
  relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from address 0.
 Instead, they count from a value called the relative base. The relative base starts at
  0.

The address a relative mode parameter refers to is itself plus the current relative
 base. When the relative base is 0, relative mode parameters and position mode
  parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7 refers to
 memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

Opcode 9 adjusts the relative base by the value of its only parameter. The relative
 base increases (or decreases, if the value is negative) by the value of the parameter.
For example, if the relative base is 2000, then after the instruction 109,19, the
 relative base would be 2019. If the next instruction were 204,-34, then the value at
  address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

The computer's available memory should be much larger than the initial program. Memory
 beyond the initial program starts with the value 0 and can be read or written like any
  other memory. (It is invalid to try to access memory at a negative address, though.)
The computer should have support for large numbers. Some instructions near the
 beginning of the BOOST program will verify this capability.
Here are some example programs that use these features:

109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a
 copy of itself as output.
1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
104,1125899906842624,99 should output the large number in the middle.
The BOOST program will ask for a single input; run it in test mode by providing it the
 value 1. It will perform a series of checks on each opcode, output any opcodes (and
  the associated parameter modes) that seem to be functioning incorrectly, and finally
   output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report no
 malfunctioning opcodes when run in test mode; it should only output a single value,
  the BOOST keycode. What BOOST keycode does it produce?

--- Part Two ---

You now have a complete Intcode computer.

Finally, you can lock on to the Ceres distress signal! You just need to boost your
 sensors using the BOOST program.

The program runs in sensor boost mode by providing the input instruction the value 2.
 Once run, it will boost the sensors automatically, but it might take a few seconds to
  complete the operation on slower hardware. In sensor boost mode, the program will
   output a single value: the coordinates of the distress signal.

Run the BOOST program in sensor boost mode. What are the coordinates of the distress
 signal?
"""
import numpy as np
from enum import Enum
from typing import List


class OpCode(Enum):
    STOP = 99


class InitMode(Enum):
    NORMAL = 0
    REPRISE = 1


class Intcode:
    """Class for IntCode"""

    def __init__(self, instructions: np.array):
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
