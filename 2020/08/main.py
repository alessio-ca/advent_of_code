import re
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


class ItsALoop(Exception):
    """Exception raised when a loop is detected"""

    pass


class ItsAMatch(Exception):
    """Exception raised when the program executes correctly"""

    pass


class LoopDetector:
    """Loop detector object"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.register = set()

    def update(self, idx):
        # If `idx` is already in the register,
        #  you are repeating an instruction
        if idx in self.register:
            raise ItsALoop
        self.register.add(idx)


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


class DummyProgram:
    """Dummy Program object"""

    def __init__(self, instructions: List[Tuple[str, int]]):
        # Initialise the objects
        self.acc = Counter()
        self.idx = Counter()
        self.loop_detector = LoopDetector()
        self.instructions = Instructions(instructions)

    def reset(self):
        # Reset the program
        self.acc.reset()
        self.idx.reset()
        self.loop_detector.reset()

    def fetch(self):
        # Fetch instructions (with loop detector)
        self.loop_detector.update(self.idx.val)
        return self.instructions.fetch(self.idx.val)

    def execute(self):
        # Execute program
        instr, arg = self.fetch()
        if instr == "acc":
            self.acc.incr(arg)
        self.idx.incr(arg if instr == "jmp" else 1)

    def run(self):
        # Run the program
        self.reset()
        while True:
            self.execute()


def main():
    input_file = read_input("2020/08/input.txt")
    # Format file
    instructions = [
        (instr, int(arg))
        for instr, arg in [
            re.match(r"(\w{3}) (\-?\d+|\+?\d+)", line).groups() for line in input_file
        ]
    ]
    # For part one, simply catch the loop and output the accumulator
    dummy_program = DummyProgram(instructions)
    try:
        dummy_program.run()
    except ItsALoop:
        acc_after_exec = dummy_program.acc.val

    print(f"Result of part 1: {acc_after_exec}")
    # For part two, change every instruction and monitor correct execution
    for idx, (instr, _) in enumerate(instructions):
        # Modify instructions
        #  (need to convert to list as tuples are immutable)
        new_instructions = [list(entry) for entry in instructions]
        if instr == "jmp":
            new_instructions[idx][0] = "nop"
        elif instr == "nop":
            new_instructions[idx][0] = "jmp"
        else:
            continue
        # Reconvert to tuples
        new_instructions = [tuple(entry) for entry in new_instructions]

        # Execute program with loop detector or correct execution
        dummy_program = DummyProgram(new_instructions)
        try:
            dummy_program.run()
        except ItsALoop:
            continue
        except ItsAMatch:
            acc_after_exec = dummy_program.acc.val
            print(f"Result of part 2: {acc_after_exec} (changing instruction {idx})")
            return -1

    # If you really didn't manage to execute after trying everything...
    print("You utterly failed! No instruction change can save this program!")


if __name__ == "__main__":
    main()
