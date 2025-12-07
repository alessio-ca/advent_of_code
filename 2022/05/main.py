import re
from typing import List, Tuple


def create_input(
    lines: List[str],
) -> Tuple[List[List[str]], List[Tuple[int, int, int]]]:
    # Parse input: first section corresponds to the stacks
    rows = []
    for i, line in enumerate(lines):
        if line == "\n":
            break
        rows.append(line[1::4])

    stacks: list[list[str]] = [[] for _ in range(len(rows.pop()))]
    while rows:
        for j, char in enumerate(rows.pop()):
            if char != " ":
                stacks[j].append(char)

    # Second section corresponds to the instructions
    instructions = []
    for line in lines[i + 1 :]:
        nums = tuple(int(s) for s in re.findall(r"\b\d+\b", line))
        if len(nums) == 3:
            instructions.append(nums)

    return stacks, instructions


def rearrange_stacks(
    stacks: List[List[str]],
    instructions: List[Tuple[int, int, int]],
    is_9001: bool = False,
):
    # Iterate over instructions
    for instruction in instructions:
        num, origin, destination = instruction
        # Pull and push crates from stacks in sequential order into a temp stack
        temp_stack = []
        for _ in range(num):
            temp_stack.append(stacks[origin - 1].pop())
        # If it is the 9001 model, reverse the stack
        if is_9001:
            temp_stack.reverse()
        # Add it to destination
        stacks[destination - 1] += temp_stack


def main(filename: str):
    with open(filename, "r") as input_file:
        lines = input_file.readlines()

    stacks, instructions = create_input(lines)
    rearrange_stacks(stacks, instructions)
    print(f"Result of part 1: {''.join([stack.pop() for stack in stacks])}")

    stacks, instructions = create_input(lines)
    rearrange_stacks(stacks, instructions, is_9001=True)
    print(f"Result of part 2: {''.join([stack.pop() for stack in stacks])}")


if __name__ == "__main__":
    main("2022/05/input.txt")
