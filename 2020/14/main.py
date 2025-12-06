import re
from itertools import product
from typing import List

from utils import read_input


class ItsAMatch(Exception):
    """Exception raised when the program executes correctly"""

    pass


class Instructions:
    """Instructions object"""

    def __init__(self, instructions: List[str]):
        self.reset()
        self.load(instructions)

    def reset(self):
        self.instructions = []

    def load(self, instructions: List[str]):
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
    def __init__(self, instructions: List[str], version):
        if version not in ["v1", "v2"]:
            raise Exception(f"The version {version} is not supported")
        self.version = version

        self.memory: dict[str, int] = {}
        self.mask = "".join(["X" for x in range(36)])
        # Process mask generating 4 objects:
        # - A binary number that serves as OR mask
        # - A binary number that serves as AND mask
        # - A list of the indexes where the mask is 'X'
        # - The possible combinations of "0" and "1" for the X positions
        self.process_mask()
        self.idx = 0
        self.instructions = Instructions(instructions)
        self.is_mask = re.compile(r"^mask = ([10X]+)$")
        self.is_mem = re.compile(r"^mem\[(\d+)\] = (\d+)$")

    def process_mask(self):
        self.mask_or = int(self.mask.replace("X", "0"), 2)
        self.mask_and = int(self.mask.replace("X", "1"), 2)
        self.floating_pos = [
            idx for idx in range(len(self.mask)) if self.mask[idx] == "X"
        ]

    def reset(self):
        # Reset the program
        self.memory = {}
        self.idx = 0
        self.mask = "".join(["X" for x in range(36)])
        self.process_mask()

    def fetch(self):
        # Fetch instructions
        return self.instructions.fetch(self.idx)

    def process(self, instr):
        mask = self.is_mask.match(instr)
        if mask:
            # Update the masks
            self.mask = mask.groups()[0]
            self.process_mask()
        else:
            # Get memory instruction
            address, number = self.is_mem.match(instr).groups()

            if self.version == "v1":
                # Set the new number
                # Do the binary logic using the OR and AND masks
                self.memory[address] = self.mask_and & (self.mask_or | int(number))

            elif self.version == "v2":
                # Obtain the temporary mask before resolving the Xs (in str form)
                temp_mask = list(f"{(self.mask_or | int(address)):036b}")
                # Resolve the Xs
                memory_addresses = []
                if self.floating_pos:
                    # If there are Xs, obtain the unique combinations
                    #  of 0-1 for the masks
                    for mask in product("01", repeat=len(self.floating_pos)):
                        # Replace the Xs with the combinations element
                        for idx, el in zip(self.floating_pos, mask):
                            temp_mask[idx] = el
                        memory_addresses.append(int("".join(temp_mask), 2))
                else:
                    # If there aren't Xs, just append the mask
                    memory_addresses.append(int("".join(temp_mask), 2))

                for address in memory_addresses:
                    # Update the number
                    self.memory[address] = int(number)

    def execute(self):
        # Execute program
        instr = self.fetch()
        self.process(instr)
        self.idx += 1

    def run(self):
        # Run the program
        self.reset()
        while True:
            self.execute()


def main():
    input_file = read_input("2020/14/input.txt")
    # For part one, run the program
    dummy_program = DummyProgram(input_file, version="v1")
    try:
        dummy_program.run()
    except ItsAMatch:
        sum_memory = sum(value for _, value in dummy_program.memory.items())
    print(f"Result of part 1: {sum_memory}")

    # For part one, run the program with version 2
    dummy_program.version = "v2"
    dummy_program.reset()
    try:
        dummy_program.run()
    except ItsAMatch:
        sum_memory = sum(value for _, value in dummy_program.memory.items())
    print(f"Result of part 2: {sum_memory}")


if __name__ == "__main__":
    main()
