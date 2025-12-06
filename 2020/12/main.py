import re
from typing import List, Tuple

import numpy as np

from utils import read_input


class ItsAMatch(Exception):
    """Exception raised when the program executes correctly"""

    pass


class Instructions:
    """Instructions object"""

    def __init__(self, instructions: List[Tuple[str, int]]):
        self.reset()
        self.load(instructions)

    def reset(self):
        self.instructions = []

    def load(self, instructions: List[Tuple[str, int]]):
        self.instructions = instructions

    def fetch(self, idx: int):
        # Fetch the instruction.
        # If IndexError is reached,
        #  no next instruction is available!
        try:
            return self.instructions[idx]
        except IndexError:
            raise ItsAMatch


class DummyShip:
    def __init__(self, instructions: List[Tuple[str, int]], mode="ship"):
        self.pos = np.array([0, 0])
        self.direction = 0
        self.way_pos = np.array([10, 1])
        self.idx = 0
        self.instructions = Instructions(instructions)
        if mode not in ["ship", "way"]:
            raise Exception(f"Ship movement mode {mode} is not valid.")
        self.mode = mode

        self.move_vectors = {
            "N": (0, 1, 0, 0),
            "S": (0, -1, 0, 0),
            "E": (1, 0, 0, 0),
            "W": (-1, 0, 0, 0),
            "L": (0, 0, 1, 0),
            "R": (0, 0, -1, 0),
            "F": (0, 0, 0, 1),
        }

    def reset(self):
        # Reset the program
        self.pos = np.array([0, 0])
        self.way_pos = np.array([10, 1])
        self.direction = 0
        self.idx = 0

    def fetch(self):
        # Fetch instructions
        return self.instructions.fetch(self.idx)

    def move(self, instr, arg):
        # Define the X, Y, rotation and forward moves
        x, y, rot, forward = self.move_vectors[instr]
        # Update direction
        self.direction += rot * arg
        self.direction %= 360
        # Define rotation matrix
        c, s = np.cos(arg * rot * np.pi / 180), np.sin(arg * rot * np.pi / 180)
        rot_matrix = np.around(np.array(((c, -s), (s, c)))).astype(int)

        if self.mode == "ship":
            # Move on X and Y
            self.pos[0] += arg * (
                x + forward * np.around(np.cos(self.direction * np.pi / 180))
            )
            self.pos[1] += arg * (
                y + forward * np.around(np.sin(self.direction * np.pi / 180))
            )
        elif self.mode == "way":
            # Move waypoint X and Y
            self.way_pos[0] += arg * x
            self.way_pos[1] += arg * y
            self.way_pos = rot_matrix.dot(self.way_pos)
            # Move ship
            self.pos = self.pos + arg * forward * self.way_pos

    def execute(self):
        # Execute program
        instr, arg = self.fetch()
        self.move(instr, arg)
        self.idx += 1

    def run(self):
        # Run the program
        self.reset()
        while True:
            self.execute()


def main():
    input_file = read_input("2020/12/input.txt")
    # Format file
    instructions = [
        (instr, int(arg))
        for instr, arg in [re.match(r"(\w)(\d+)", line).groups() for line in input_file]
    ]
    # For part one, run the program with mode "ship"
    dummy_ship = DummyShip(instructions, mode="ship")
    try:
        dummy_ship.run()
    except ItsAMatch:
        man_distance = np.abs(dummy_ship.pos).sum()
    print(f"Result of part 1: {man_distance}")

    # For part two, run the program with mode "way"
    dummy_ship.reset()
    dummy_ship.mode = "way"
    try:
        dummy_ship.run()
    except ItsAMatch:
        man_distance = np.abs(dummy_ship.pos).sum()
    print(f"Result of part 2: {man_distance}")


if __name__ == "__main__":
    main()
