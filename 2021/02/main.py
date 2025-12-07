from typing import List, Tuple

from utils import read_input


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
    try:
        pilot_program.run()
    except EndExec:
        res_2 = pilot_program.depth.val * pilot_program.pos.val

    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main()
