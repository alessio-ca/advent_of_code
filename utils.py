from typing import List


def read_input(input_file: str) -> List[str]:
    with open(input_file, "r") as input_file:
        input_list = []
        for line in input_file:
            input_list.append(line.strip())

    return input_list


def read_input_batch(input_file: str, line_split: bool = True) -> List[str]:
    with open(input_file, "r") as input_file:
        input_list = []
        batch = []
        for line in input_file:
            if line == "\n":
                input_list.append(batch)
                batch = []
            else:
                if line_split:
                    for element in line.strip().split(" "):
                        batch.append(element)
                else:
                    batch.append(line.strip())

        # Append last batch
        if batch:
            input_list.append(batch)

    return input_list
