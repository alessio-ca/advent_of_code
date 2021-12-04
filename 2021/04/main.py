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
    game_1 = BingoGame(X, numbers, mode=1)
    number, winning_sum = game_1.run()
    print(f"Result of part 1: {winning_sum * number}")

    # Obtain the last board to win
    game_2 = BingoGame(X, numbers, mode=2)
    number, winning_sum = game_2.run()
    print(f"Result of part 2: {winning_sum * number}")


if __name__ == "__main__":
    main()
