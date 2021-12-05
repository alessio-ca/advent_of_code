"""
--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean, already so
 deep that you can't see any sunlight. What you can see, however, is a giant squid that
  has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are
 chosen at random, and the chosen number is marked on all boards on which it appears.
  (Numbers may not appear on all boards.) If all numbers in any row or any column of a
   board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant
 squid) pass the time. It automatically generates a random order in which to draw
  numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but
 the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no
 winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column
 of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all
 unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum
  by the number that was just called when the board won, 24, to get the final score,
   188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first.
 What will your final score be if you choose that board?

--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant squid
 win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than
 waste time counting its arms, the safe thing to do is to figure out which board will
  win last and choose that one. That way, no matter which boards it picks, it will win
   for sure.

In the above example, the second board is the last to win, which happens after 13 is
 eventually called and its middle column is completely marked. If you were to keep
  playing until this point, the second board would have a sum of unmarked numbers equal
   to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

"""
from utils import read_input_batch
import numpy as np


class BingoGame:
    def __init__(self, boards: np.ndarray, numbers: np.ndarray, mode: int):
        # Initialise the objects
        self.boards = boards
        self.numbers = numbers
        self.mode = mode

    def reset(self):
        # Reset the boards
        self.X = self.boards.copy()

    def to_win(self, axis: int):
        # Check if a board wins. Return the board number (-1 if there is no winner yet)
        if np.any(self.X.sum(axis=axis) == 0):
            return np.where(self.X.sum(axis=axis) == 0)[0][0]
        else:
            return -1

    def first_winning_board(self):
        # Obtain the first winning board, if we have it
        # Return the board number (-1 if there is no winner yet)
        for axis in [1, 2]:
            winning_table = self.to_win(axis=axis)
            if winning_table:
                return winning_table
        return -1

    def last_winning_board(self):
        # Obtain the last winning board, if we have it
        # Return the board number (-1 if there is no final winning board yet)
        for axis in [1, 2]:
            winning_table = self.to_win(axis=axis)
            if winning_table >= 0:
                # Delete the winning board if there are still others
                if self.X.shape[0] != 1:
                    self.X = np.delete(self.X, winning_table, axis=0)
                # Otherwise, return the last winning board
                else:
                    return winning_table
        return -1

    def run(self):
        # Run the program
        self.reset()

        # Set the win_condition function
        if self.mode == 1:
            win_condition = self.first_winning_board
        elif self.mode == 2:
            win_condition = self.last_winning_board
        else:
            raise ValueError

        # Loop over the numbers
        for number in self.numbers:
            self.X[self.X == number] = 0
            candidate = win_condition()
            if candidate >= 0:
                return number, self.X[candidate].sum()
            else:
                pass

        return -1, -1


def main():
    input_file = read_input_batch("2021/04/input.txt")
    numbers = np.array(input_file[0][0].split(","), dtype=int)
    matrices = input_file[1:]
    # Process matrices
    X = np.empty(shape=(len(matrices), 5, 5), dtype=int)
    for i, matrix in enumerate(matrices):
        # Remove empty characters
        matrix = [el for el in matrix if el != ""]
        X[i] = np.array(matrix).reshape(5, 5)

    # Obtain the first board to win
    game = BingoGame(X, numbers, mode=1)
    number, winning_sum = game.run()
    print(f"Result of part 1: {winning_sum * number}")

    # Obtain the last board to win
    game.mode = 2
    number, winning_sum = game.run()
    print(f"Result of part 2: {winning_sum * number}")


if __name__ == "__main__":
    main()
