"""
--- Day 12: Rain Risk ---

Your ferry made decent progress toward the island, but the storm came in
 faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning;
 rather than giving a route directly to safety, it produced extremely
  circuitous instructions. When the captain uses the PA system to ask if
   anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of
 single-character actions paired with integer input values. After staring at
  them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is
 currently facing.
The ship starts by facing east. Only the L and R actions change the direction
 the ship is facing. (That is, if the ship is facing east and the next
  instruction is N10, the ship would move north 10 units, but would still move
   east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east)
 to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing
 east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it
 remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the
 absolute values of its east/west position and its north/south position) from
  its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan
 distance between that location and the ship's starting position?

--- Part Two ---

Before you can give the destination to the captain, you realize that the
 actual action meanings were printed on the back of the instructions the whole
  time.

Almost all of the actions indicate how to move a waypoint which is relative to
 the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise)
 the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the
 given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the
 given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The
 waypoint is relative to the ship; that is, if the ship moves, the waypoint
  moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10
 units north), leaving the ship at east 100, north 10. The waypoint stays 10
  units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the
 ship. The ship remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28
 units north), leaving the ship at east 170, north 38. The waypoint stays 10
  units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4
 units east and 10 units south of the ship. The ship remains at east 170,
  north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110
 units south), leaving the ship at east 214, south 72. The waypoint stays 4
  units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting
 position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the
 Manhattan distance between that location and the ship's starting position?
"""
from utils import read_input
import re
from typing import List, Tuple
import numpy as np


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
    def __init__(self, instructions: List[Tuple[str, int]], mode='ship'):
        self.pos = np.array([0, 0])
        self.direction = 0
        self.way_pos = np.array([10, 1])
        self.idx = 0
        self.instructions = Instructions(instructions)
        if mode not in ['ship', 'way']:
            raise Exception(f'Ship movement mode {mode} is not valid.')
        self.mode = mode

        self.move_vectors = {
            "N": (0, 1, 0, 0),
            "S": (0, -1, 0, 0),
            "E": (1, 0, 0, 0),
            "W": (-1, 0, 0, 0),
            "L": (0, 0, 1, 0),
            "R": (0, 0, -1, 0),
            "F": (0, 0, 0, 1)
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

        if self.mode == 'ship':
            # Move on X and Y
            self.pos[0] += arg * (
                x + forward * np.around(np.cos(self.direction * np.pi / 180))
            )
            self.pos[1] += arg * (
                y + forward * np.around(np.sin(self.direction * np.pi / 180))
            )
        elif self.mode == 'way':
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
    # fmt: off
    instructions = [
        (instr, int(arg))
        for instr, arg in [
            re.match(r"(\w)(\d+)", line).groups()
            for line in input_file
        ]
    ]
    # For part one, run the program with mode "ship"
    dummy_ship = DummyShip(instructions, mode='ship')
    try:
        dummy_ship.run()
    except ItsAMatch:
        man_distance = np.abs(dummy_ship.pos).sum()
    print(f"Result of part 1: {man_distance}")

    # For part two, run the program with mode "way"
    dummy_ship.reset()
    dummy_ship.mode = 'way'
    try:
        dummy_ship.run()
    except ItsAMatch:
        man_distance = np.abs(dummy_ship.pos).sum()
    print(f"Result of part 2: {man_distance}")


if __name__ == "__main__":
    main()
