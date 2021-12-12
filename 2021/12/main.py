from collections import defaultdict
from typing import DefaultDict, List, Tuple
from utils import read_input


def find_paths(
    start: str,
    current_counter: DefaultDict[str, int],
    edge_dict: DefaultDict[str, List[str]],
    point_list: List[Tuple[str, str]],
    twice: bool = False,
) -> int:
    """Recursive function to find paths"""
    # Define path dictionary based on current one
    future_counter = defaultdict(int, current_counter)
    future_counter[start] += 1
    # Check if we reached the start
    if start == "start":
        return 1
    # Or we looped at the end
    elif start == "end":
        return 0
    # Or if we are visiting a small cave twice
    elif (start.islower()) and (future_counter[start] > 1):
        if not twice:
            return 0
        else:
            # Check if it's the first small cave we visited twice
            if any(
                current_counter[small_cave] > 1
                for small_cave in current_counter.keys()
                if small_cave.islower()
            ):
                return 0
            else:
                pass

    # Else, apply recursion
    return sum(
        find_paths(new_start, future_counter, edge_dict, point_list, twice)
        for new_start in edge_dict[start]
    )


def main():
    input_file = [tuple(line.split("-")) for line in read_input("2021/12/input.txt")]
    # Create dictionary of edges
    edge_dict = defaultdict(list)
    for edge in input_file:
        edge_dict[edge[0]].append(edge[1])
        edge_dict[edge[1]].append(edge[0])

    res_1 = sum(
        find_paths(point, defaultdict(int), edge_dict, input_file)
        for point in edge_dict["end"]
    )
    print(f"Result of part 1: {res_1}")
    res_2 = sum(
        find_paths(point, defaultdict(int), edge_dict, input_file, twice=True)
        for point in edge_dict["end"]
    )
    print(f"Result of part 1: {res_2}")


if __name__ == "__main__":
    main()
