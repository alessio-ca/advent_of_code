from utils import read_input, timefunc
import re
from itertools import product
from collections import Counter
import numpy as np
from typing import List, Tuple


class Player:
    def __init__(self, id: int, start_pos: int):
        self.id = id
        self.x = start_pos
        self.score = 0

    def move(self, roll: int):
        # Move
        self.x += roll
        # Normalize
        self.x = self.x % 10
        # Obtain new score
        new_score = self.x if self.x > 0 else 10
        self.score += new_score

        return self


class QuantumPlayer:
    def __init__(self, id: int, start_pos: int, counter: Counter):
        self.id = id
        self.counter = counter
        self.step = 0

        self.positions = np.zeros(shape=(10,), dtype=int)
        self.positions[start_pos] = 1  # One universe in starting position

        self.scores = np.zeros(shape=(10, 21), dtype=int)
        self.scores[start_pos, 0] = 1  # One universe with score 0 in starting position

        # Internal arrays
        self._new_positions = np.zeros(shape=(10,), dtype=int)
        self._accumulator = np.zeros(shape=(10,), dtype=int)
        self._winners = np.zeros(shape=(10,), dtype=int)
        self._new_scores = np.zeros(shape=(10, 21), dtype=int)
        self._tot_winners = 0

        # List of starters, winners and still playing at each winning step
        self.results = []

    def create_new_positions(self, pos):
        # Create new positions based on current position and all possible outcomes
        for roll, n in self.counter.items():
            result = (pos + roll) % 10
            self._accumulator[result] += 1 * n
        return self

    def update_scores(self, pos: int, past_score: int, n_past: int):
        # Loop over the newly found positions in accumulator
        for new_pos, n_new in enumerate(self._accumulator):
            # If there are universes
            if n_new > 0:
                new_score = new_pos if new_pos != 0 else 10
                # If the new score is larger than 21, add to the winning list and record the step
                if past_score + new_score >= 21:
                    self._winners[new_pos] += n_new * n_past
                    self._tot_winners += n_new * n_past
                # Else, update the scores for the new position
                else:
                    self._new_scores[new_pos, past_score + new_score] += n_new * n_past
        # Substract the number of updated universes from the old position
        self._new_scores[pos, past_score] -= n_past
        return self

    def move_per_position(self, pos: int, n_universes: int):
        # Reset accumulator
        self._accumulator[:] = 0
        # Reset winners per move
        self._winners[:] = 0
        # If there are universes in this position
        if n_universes > 0:
            # Create array of new positions based on the 27 possible outcomes in Counter
            self.create_new_positions(pos)
            # For each of these new positions, update corresponding scores & record eventual winners
            for past_score, n_past in enumerate(self.scores[pos]):
                # If there are universes with this score
                if n_past > 0:
                    self.update_scores(pos, past_score, n_past)

        # Add accumulator to the new positions
        self._new_positions += n_universes * self._accumulator
        # Subtract winners
        self._new_positions -= self._winners
        # Subtract the old counter
        self.positions[pos] -= n_universes
        return self

    def move(self):
        # Move
        initial_number = self.positions.sum()
        # Reset temp matrix of the new scores
        self._new_scores[:] = 0
        # Reset temp array of the new positions
        self._new_positions[:] = 0
        # Instantiate temp variable to record the number of winnings
        self._tot_winners = 0

        # Do move for each possible universe position
        for position, n_universes in enumerate(self.positions):
            self.move_per_position(position, n_universes)

        #  Update the positions
        self.positions += self._new_positions
        #  Update the scores
        self.scores += self._new_scores
        # If there are winners this round, record the step, number of winners, current
        #  number of universes and initial number of universes
        if self._tot_winners > 0:
            self.results.append(
                (self.step, self._tot_winners, self.positions.sum(), initial_number)
            )
            self.step += 1

        return self

    def play(self) -> List[Tuple]:
        # Keep playing until there are universes
        while self.positions.sum() > 0:
            self.move()

        # Return the results
        return self.results


def who_wins_more(player_1: QuantumPlayer, player_2: QuantumPlayer) -> int:
    total_1 = 0
    total_2 = 0
    # Query the results of the two players
    for (status_1, status_2) in zip(player_1.results, player_2.results):
        # Assign quantities from status at each step
        _, winners_1, playing_1, _ = status_1
        _, winners_2, _, beginning_2 = status_2

        # The number of universes where player 1 wins is the number of winners per the
        #  number of universes at the beginning for player 2 (since player 1 moves
        #  first)
        total_1 += winners_1 * beginning_2
        # The number of universes where player 2 wins is the number of winners per the
        #  number of universes still playing for player 1 (since player 2 moves last)
        total_2 += winners_2 * playing_1

    return max(total_1, total_2)


@timefunc
def main():
    input_file = read_input("2021/21/input.txt")
    data_1, data_2 = [
        tuple(map(int, re.findall("[0-9]+", line))) for line in input_file
    ]

    player_1 = Player(*data_1)
    player_2 = Player(*data_2)

    # With fair dice
    dice_roll = -3
    turn = True
    n = 0
    while (player_1.score < 1000) & (player_2.score < 1000):
        n += 3
        dice_roll += 9
        if turn:
            # It's player 1
            player_1.move(dice_roll)
        else:
            # It's player 2
            player_2.move(dice_roll)
        turn = not turn

    loser_score = min(player_1.score, player_2.score)
    print(f"Result of part 1: {loser_score * n}")

    # Obtain the number of possible outcomes per triplet of rolls. Create a counter
    counter = Counter([sum(rolls) + 3 for rolls in list(product(range(3), repeat=3))])

    player_1 = QuantumPlayer(*data_1, counter)
    player_2 = QuantumPlayer(*data_2, counter)
    player_1.play()
    player_2.play()
    print(f"Result of part 2: {who_wins_more(player_1, player_2)}")


if __name__ == "__main__":
    main()
