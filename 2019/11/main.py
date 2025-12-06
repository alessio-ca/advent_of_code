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


def colour_and_turn(intcode: Intcode, grid: np.ndarray):
    """Convenience function to implement the colour&turn loop"""
    # Initialize position, direction and rotation arrays
    grid_size, _ = grid.shape
    pos = np.array([grid_size // 2, grid_size // 2])
    direction = np.array([0, 1])
    R = np.array([[0, -1], [1, 0]])

    # Keep track of visited positions
    set_visited = set()
    # Set the initial turn command to 0
    turn = 0
    while turn != OpCode.STOP:
        # Run in reprise mode -- repeat the input twice to be consistent with the
        #  reprise mode implementation
        x, y = pos
        in_color = grid[x, y]
        intcode.init_mode(InitMode.REPRISE, [in_color, in_color])
        # Fetch color
        color = intcode.run()
        if color == OpCode.STOP:
            break
        # Update color
        grid[x, y] = color
        # Add to visited positions
        set_visited.add((x, y))
        # Fetch turn
        turn = intcode.run()
        # Update direction
        if turn == 0:
            direction = R.dot(direction)
        elif turn == 1:
            direction = -R.dot(direction)
        else:
            raise Exception(f"Turn {turn} is not recognized.")
        # Update grid
        pos = pos + direction

    return set_visited, grid


def main():
    input_array = np.loadtxt("2019/11/input.txt", delimiter=",", dtype=np.int64)
    instructions = input_array.copy()

    # Init intcode
    intcode = Intcode(instructions)

    # Initialize grid -- part 1
    grid = np.zeros(shape=(1001, 1001), dtype=np.int64)

    set_visited, _ = colour_and_turn(intcode, grid)

    print(f"Result of part 1: {len(set_visited)}")

    # Initialize grid -- part 2
    intcode.reset()
    grid = np.zeros(shape=(1001, 1001), dtype=np.int64)
    grid[500, 500] = 1

    set_visited, grid = colour_and_turn(intcode, grid)
    # Find first and last non-zero row and column
    zero_rows = np.where(grid.sum(axis=1) != 0)[0]
    zero_cols = np.where(grid.sum(axis=0) != 0)[0]
    grid = grid[
        zero_rows[0] - 1 : zero_rows[-1] + 2, zero_cols[0] - 1 : zero_cols[-1] + 2
    ]
    # Get final image
    map_to_pixel = {0: " ", 1: "#"}
    decoded = ""
    for row in np.rot90(grid):
        decoded += "".join(map(map_to_pixel.get, row)) + "\n"
    print("Result of part 2: ")
    print("")
    print(f"{decoded}")


if __name__ == "__main__":
    import cProfile

    cProfile.run("main()")
