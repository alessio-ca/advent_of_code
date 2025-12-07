from collections import deque
from typing import Deque, Dict

from utils import read_input


def create_result_dictionary(
    results: Deque[int], right_rotate: bool
) -> Dict[str, Dict[str, int]]:
    opponent_choice = ["A", "B", "C"]
    player_choice = ["X", "Y", "Z"]
    results_dict = {}
    for input in opponent_choice:
        results_dict[input] = dict(zip(player_choice, list(results)))
        results.rotate(1 if right_rotate else -1)
    return results_dict


def main(filename: str):
    X_raw = read_input(filename, line_strip=False)
    X = [line.split(" ") for line in X_raw]

    # Create results and choices dictionary
    results = deque([3, 6, 0])
    results_dict = create_result_dictionary(results, right_rotate=True)
    choices_dict = {"X": 1, "Y": 2, "Z": 3}
    # Calculate results and choices scores
    total_score = 0
    for opponent, player in X:
        total_score += results_dict[opponent][player] + choices_dict[player]
    print(f"Result of part 1: {total_score}")

    # Create results and choices dictionary
    results = deque([3, 1, 2])
    results_dict = create_result_dictionary(results, right_rotate=False)
    choices_dict = {"X": 0, "Y": 3, "Z": 6}
    # Calculate results and choices scores
    total_score = 0
    for opponent, player in X:
        total_score += results_dict[opponent][player] + choices_dict[player]
    print(f"Result of part 2: {total_score}")


if __name__ == "__main__":
    main("2022/02/input.txt")
