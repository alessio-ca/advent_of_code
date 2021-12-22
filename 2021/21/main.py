from utils import read_input, timefunc
import re
from itertools import product
from collections import Counter
import numpy as np
from numpy.fft import fft, ifft


def _roll_rows(A, r):
    """Roll rows of a matrix on the right by a row-specific amount specified in r"""
    return np.real(
        ifft(
            fft(A, axis=1)
            * np.exp(
                -2
                * 1j
                * np.pi
                / A.shape[1]
                * r[:, None]
                * np.r_[0 : A.shape[1]][None, :]
            ),
            axis=1,
        ).round()
    ).astype(A.dtype)


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

        self.scores = np.zeros(shape=(10, 21), dtype=int)
        self.scores[start_pos, 0] = 1  # One universe with score 0 in starting position

        # Internal arrays
        self._accumulator = np.zeros(shape=(10, 21), dtype=int)
        self._tot_winners = 0

        # List of starters, winners and still playing at each winning step
        self.results = []

    def create_accumulator(self):
        # Create new positions based on current position and all possible outcomes
        for roll, n in self.counter.items():
            for pos in np.arange(self.scores.shape[0]):
                result = (pos + roll) % 10
                # Each row of the accumulator is increased by the number of outcomes per
                #  this new position per the row of scores at pos (so if there are no
                #  universes/a pos/score combination is empty, it will not be
                #  accumulated)

                #  Can be vectorized by moving the pos -> result mapping (as it is a
                #  function) to a lookup table
                self._accumulator[result, :] += 1 * n * self.scores[pos, :]
        return self

    def update_scores(self):
        # Calculate array of new scores (position, or 10 if position is 0)
        new_scores = np.arange(self.scores.shape[0])
        new_scores[0] = 10

        # Only rows and columns where column + (new score) < 21 are valid
        mask = (
            np.arange(self.scores.shape[1])[np.newaxis, :] + new_scores[:, np.newaxis]
            >= 21
        )

        # Record the number of winners and remove them from accumulator
        self._tot_winners = self._accumulator[mask].sum()
        self._accumulator[mask] = 0

        # Set the accumulator to be the new scores by shifting
        self.scores = _roll_rows(self._accumulator, new_scores)
        return self

    def move_per_position(self):
        # Reset accumulator
        self._accumulator[:] = 0
        # Create accumulator of new positions based on the 27 possible outcomes
        #  in self.counter
        self.create_accumulator()
        # For each of these new positions, update corresponding scores & record
        #  eventual winners
        self.update_scores()
        return self

    def move(self):
        # Update the step
        self.step += 1

        # Record initial number of universes
        initial_number = self.scores.sum()
        # Reset count of winners this round
        self._tot_winners = 0

        # Do move for each possible universe position
        # Get current positions with existing universes
        self.move_per_position()

        # If there are winners this round, record the step, number of winners, current
        #  number of universes and initial number of universes
        if self._tot_winners > 0:
            self.results.append(
                (self.step, self._tot_winners, self.scores.sum(), initial_number)
            )
        return self

    def play(self):
        # Keep playing until there are universes
        while self.scores.sum() > 0:
            self.move()

        return self


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

    print(f"Result of part 1: {min(player_1.score, player_2.score) * n}")

    # Obtain the number of possible outcomes per triplet of rolls. Create a counter
    counter = Counter([sum(rolls) + 3 for rolls in list(product(range(3), repeat=3))])

    # Set up the two players. Play individually (since each player is independent, and
    #  we only need to compare the results at the end of each round)
    player_1 = QuantumPlayer(*data_1, counter)
    player_2 = QuantumPlayer(*data_2, counter)
    player_1.play()
    player_2.play()
    # Find winner based on the results of each individual player at each round
    print(f"Result of part 2: {who_wins_more(player_1, player_2)}")


if __name__ == "__main__":
    main()
