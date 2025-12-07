from collections import defaultdict
from typing import DefaultDict, List, Tuple

from utils import read_input


def find_paths(
    start: str,
    current_counter: DefaultDict[str, int],
    edge_dict: DefaultDict[str, List[str]],
    point_list: List[Tuple[str, str]],
    twice: bool = False,
    double: bool = False,
) -> int:
    """Recursive function to find paths"""
    # Define path dictionary based on current one
    future_counter = defaultdict(int, current_counter)
    future_counter[start] += 1
    # Check if we reached the start
    if start == "start":
        return 1
    # Or if we are visiting a small cave twice
    elif (start.islower()) and (future_counter[start] > 1):
        # If twice is not allowed, or it is the second, path is not valid
        if (not twice) | double:
            return 0
        # Else, update the `double` flag
        else:
            double = True

    # Else, apply recursion
    return sum(
        find_paths(new_start, future_counter, edge_dict, point_list, twice, double)
        for new_start in edge_dict[start]
    )


def main():
    input_file = [tuple(line.split("-")) for line in read_input("2021/12/input.txt")]
    # Create dictionary of edges
    edge_dict = defaultdict(list)
    for edge_1, edge_2 in input_file:
        # Exclude start and end from root and nodes respectively
        if (edge_1 != "start") and (edge_2 != "end"):
            edge_dict[edge_1].append(edge_2)
        if (edge_2 != "start") and (edge_1 != "end"):
            edge_dict[edge_2].append(edge_1)

    res_1 = sum(
        find_paths(point, defaultdict(int), edge_dict, input_file)
        for point in edge_dict["end"]
    )
    print(f"Result of part 1: {res_1}")
    res_2 = sum(
        find_paths(point, defaultdict(int), edge_dict, input_file, twice=True)
        for point in edge_dict["end"]
    )
    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main()
