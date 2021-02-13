from typing import List


def read_input(input_file: str) -> List[str]:
    with open(input_file, "r") as input_file:
        input_list = []
        for line in input_file:
            input_list.append(line.strip())

    return input_list
