from collections import defaultdict
from itertools import accumulate
from typing import List


def read_line(commands: List[str]) -> None:
    # Initialise folder size dictionary
    folder_sizes = defaultdict(lambda: 0)
    # Initialise root structure as a list and separation marker for `cd`
    root_structure = [""]
    sep_idx = 5

    # Iterate over commands (skip first one)
    for command in commands[1:]:
        # If command starts with a number, it's a file size
        if command[0].isdigit():
            file = command.split(" ")
            # Update folder size of all the parent folders
            for folder in accumulate(root_structure, lambda a, b: "/".join([a, b])):
                folder_sizes[folder] += int(file[0])
        # If command is `cd`, we navigate the tree
        elif command[:sep_idx] == "$ cd ":
            # If `..` follows, we go up one level - remove the last element of
            #  root structure
            if command[sep_idx:] == "..":
                root_structure.pop()
            # Otherwise, add the level to root structure
            else:
                root_structure.append(command[5:])

    return folder_sizes


def main(filename: str):
    with open(filename) as f:
        commands = f.read().splitlines()
        folder_sizes = read_line(commands)
        print(
            "Result of part 1: "
            f"{sum(value for _, value in folder_sizes.items() if value <= 100000)}"
        )
        min_space = folder_sizes[""] - 40000000
        print(
            "Result of part 2: "
            f"{min(value for _, value in folder_sizes.items() if value >= min_space)}"
        )


if __name__ == "__main__":
    main("2022/07/input.txt")
