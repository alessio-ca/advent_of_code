from typing import Tuple, List, Any
from utils import read_input
import math
import re


def parse_games(games: List[str]) -> Tuple[List[int], List[Any]]:
    # Split on colon
    games_split = [re.split(r": ", game) for game in games]
    game_ids = []
    game_rounds = []
    # Loop over games
    for game_id, game_round in games_split:
        # Extract ID
        if (match := re.search(r"\d+", game_id)) is not None:
            game_ids.append(int(match.group(0)))
        else:
            raise ValueError("Missing game id")

        # Extract game rounds
        game_round = re.split(r"; ", game_round)
        game_rounds.append(
            [
                re.findall(r"(\d+)(?: )(red|blue|green)(?:, )?", round)
                for round in game_round
            ]
        )
    return game_ids, game_rounds


DICT_COLORS = {"red": 12, "green": 13, "blue": 14}


def is_valid(game):
    """Check if a game is valid"""
    for round in game:
        for number, color in round:
            if int(number) > DICT_COLORS[color]:
                return False
    return True


def min_possible_set(game):
    """Compute minimum possible set of cubes for a game"""
    min_set = {"red": 0, "green": 0, "blue": 0}
    for round in game:
        for number, color in round:
            min_set[color] = max(min_set[color], int(number))
    return min_set


def main(filename: str):
    games = read_input(filename)
    games_ids, game_rounds = parse_games(games)
    res_1 = 0
    res_2 = 0
    for game_id, game in zip(games_ids, game_rounds):
        res_1 += game_id if is_valid(game) else 0
        res_2 += math.prod(min_possible_set(game).values())

    print(f"Result of part 1: {res_1}")
    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main("2023/02/input.txt")
