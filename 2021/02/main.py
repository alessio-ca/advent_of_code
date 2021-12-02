"""
--- Day 2: Dive! ---

Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2,
 or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have
 the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input).
 You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2
Your horizontal position and depth both start at 0. The steps above would then modify
 them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a
 depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned
 course. What do you get if you multiply your final horizontal position by your final
  depth?

--- Part Two ---

Based on your calculations, the planned course doesn't seem to make any sense. You find
 the submarine manual and discover that the process is actually slightly more
  complicated.

In addition to horizontal position and depth, you'll also need to track a third value,
 aim, which also starts at 0. The commands also mean something entirely different than
  you first thought:

down X increases your aim by X units.
up X decreases your aim by X units.
forward X does two things:
It increases your horizontal position by X units.
It increases your depth by your aim multiplied by X.
Again note that since you're on a submarine, down and up do the opposite of what you
 might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your
 depth does not change.
down 5 adds 5 to your aim, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your
 depth increases by 8*5=40.
up 3 decreases your aim by 3, resulting in a value of 2.
down 8 adds 8 to your aim, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10,
 your depth increases by 2*10=20 to a total of 60.
After following these new instructions, you would have a horizontal position of 15 and a
 depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and
 depth you would have after following the planned course. What do you get if you
  multiply your final horizontal position by your final depth?
"""
from utils import read_input
from typing import List, Tuple


class Counter:
    """Counter object"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0

    def incr(self, arg):
        self.val += arg


class EndExec(Exception):
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
            raise EndExec


class PilotProgram:
    def __init__(self, instructions: List[Tuple[str, int]], mode: int):
        # Initialise the objects
        self.idx = Counter()
        self.depth = Counter()
        self.pos = Counter()
        self.aim = Counter()
        self.instructions = Instructions(instructions)
        self.mode = mode

    def reset(self):
        # Reset the program
        self.idx.reset()
        self.depth.reset()
        self.pos.reset()
        self.aim.reset()

    def fetch(self):
        # Fetch instructions
        return self.instructions.fetch(self.idx.val)

    def execute_1(self):
        # Execute program
        instr, arg = self.fetch()
        if instr == "up":
            self.depth.incr(-arg)
        elif instr == "down":
            self.depth.incr(arg)
        else:
            self.pos.incr(arg)
        self.idx.incr(1)

    def execute_2(self):
        # Execute program
        instr, arg = self.fetch()
        if instr == "up":
            self.aim.incr(-arg)
        elif instr == "down":
            self.aim.incr(arg)
        else:
            self.pos.incr(arg)
            self.depth.incr(self.aim.val * arg)
        self.idx.incr(1)

    def run(self):
        # Run the program
        self.reset()
        if self.mode == 1:
            while True:
                self.execute_1()
        elif self.mode == 2:
            while True:
                self.execute_2()
        else:
            raise ValueError


def main():
    input_file = read_input("2021/02/input.txt")
    # Format file
    instructions = [
        (instr, int(arg)) for instr, arg in [line.split(" ") for line in input_file]
    ]
    # For part one, execute the PilotProgram with mode 1
    pilot_program = PilotProgram(instructions, 1)
    try:
        pilot_program.run()
    except EndExec:
        res_1 = pilot_program.depth.val * pilot_program.pos.val

    print(f"Result of part 1: {res_1}")

    # For part two, execute the PilotProgram with mode 2
    pilot_program.mode = 2
    pilot_program.reset()

    try:
        pilot_program.run()
    except EndExec:
        res_2 = pilot_program.depth.val * pilot_program.pos.val

    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main()
