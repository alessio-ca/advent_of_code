"""
--- Day 14: Docking Data ---

As your ferry approaches the sea port, the captain asks for your help again. The
 computer system that runs this port isn't compatible with the docking program on the
  ferry, so the docking parameters aren't being correctly initialized in the docking
   program's memory.

After a brief inspection, you discover that the sea port's computer system uses a
 strange bitmask system in its initialization program. Although you don't have the
  correct decoder chip handy, you can emulate it in software!

The initialization program (your puzzle input) can either update the bitmask or write a
 value to memory. Values and memory addresses are both 36-bit unsigned integers. For
  example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the
   value 11 to memory address 8.

The bitmask is always given as a string of 36 bits, written with the most significant
 bit (representing 2^35) on the left and the least significant bit (2^0, that is, the
  1s bit) on the right. The current bitmask is applied to values immediately before
   they are written to memory: a 0 or 1 overwrites the corresponding bit in the value,
    while an X leaves the bit in the value unchanged.

For example, consider the following program:

mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
This program starts by specifying a bitmask (mask = ....). The mask it specifies will
 overwrite two bits in every written value: the 2s bit is overwritten with 0, and the
  64s bit is overwritten with 1.

The program then attempts to write the value 11 to memory address 8. By expanding
 everything out to individual bits, the mask is applied as follows:

value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
So, because of the mask, the value 73 is written to memory address 8 instead. Then, the
 program tries to write 101 to address 7:

value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)
This time, the mask has no effect, as the bits it overwrote were already the values the
 mask tried to set. Finally, the program tries to write 0 to address 8:

value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)
64 is written to address 8 instead, overwriting the value that was there previously.

To initialize your ferry's docking program, you need the sum of all values left in
 memory after the initialization program completes. (The entire 36-bit address space
  begins initialized to the value 0 at every address.) In the above example, only two
   values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing
    a sum of 165.

Execute the initialization program. What is the sum of all values left in memory after
 it completes? (Do not truncate the sum to 36 bits.)

--- Part Two ---

For some reason, the sea port's computer system still can't communicate with your
 ferry's docking program. It must be using version 2 of the decoder chip!

A version 2 decoder chip doesn't modify the values being written at all. Instead, it
 acts as a memory address decoder. Immediately before a value is written to memory,
  each bit in the bitmask modifies the corresponding bit of the destination memory
   address in the following way:

If the bitmask bit is 0, the corresponding memory address bit is unchanged.
If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
If the bitmask bit is X, the corresponding memory address bit is floating.
A floating bit is not connected to anything and instead fluctuates unpredictably.
 In practice, this means the floating bits will take on all possible values,
  potentially causing many memory addresses to be written all at once!

For example, consider the following program:

mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
When this program goes to write to memory address 42, it first applies the bitmask:

address: 000000000000000000000000000000101010  (decimal 42)
mask:    000000000000000000000000000000X1001X
result:  000000000000000000000000000000X1101X
After applying the mask, four bits are overwritten, three of which are different, and
 two of which are floating. Floating bits take on every possible combination of values;
  with two floating bits, four actual memory addresses are written:

000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
000000000000000000000000000000111010  (decimal 58)
000000000000000000000000000000111011  (decimal 59)
Next, the program is about to write to memory address 26 with a different bitmask:

address: 000000000000000000000000000000011010  (decimal 26)
mask:    00000000000000000000000000000000X0XX
result:  00000000000000000000000000000001X0XX
This results in an address with three floating bits, causing writes to eight memory
 addresses:

000000000000000000000000000000010000  (decimal 16)
000000000000000000000000000000010001  (decimal 17)
000000000000000000000000000000010010  (decimal 18)
000000000000000000000000000000010011  (decimal 19)
000000000000000000000000000000011000  (decimal 24)
000000000000000000000000000000011001  (decimal 25)
000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
The entire 36-bit address space still begins initialized to the value 0 at every
 address, and you still need the sum of all values left in memory at the end of the
  program. In this example, the sum is 208.

Execute the initialization program using an emulator for a version 2 decoder chip. What
 is the sum of all values left in memory after it completes?
"""
from utils import read_input
from typing import List
import re
from itertools import product


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

        self.memory = {}
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
