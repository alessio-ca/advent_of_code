from typing import List, Tuple

from utils import read_input

DICT_OC = {"(": ")", "[": "]", "{": "}", "<": ">"}
DICT_POINTS_CORRUPT = {")": 3, "]": 57, "}": 1197, ">": 25137}
DICT_POINTS_INCOMPLETE = {")": 1, "]": 2, "}": 3, ">": 4}


class LineIterator:
    def __init__(self):
        pass

    def _reset(self):
        self.opened = []
        self.wrong_scores = []
        self.incomplete_scores = []

    def handle_wrong(self, char: str):
        last_open = self.opened.pop()
        #  If char matches the closing of the last element, return True
        if char == DICT_OC[last_open]:
            return True
        # Else, line is corrupted. Add score to list & reset the opened list.
        #  Return False
        else:
            self.wrong_scores.append(DICT_POINTS_CORRUPT[char])
            self.opened = []
            return False

    def handle_incomplete(self):
        # If the opened list is not empty, it is an incomplete line
        if len(self.opened):
            # Obtain closing sequence
            closing_sequence = [DICT_OC[char] for char in self.opened]
            # Obtain score & append to list
            score = 0
            while len(closing_sequence):
                score = (5 * score) + DICT_POINTS_INCOMPLETE[closing_sequence.pop()]
            self.incomplete_scores.append(score)
        return self

    def iterate_line(self, line: str):
        self.opened = []
        for char in line:
            # If char is an opening character, add to list
            if char in DICT_OC.keys():
                self.opened.append(char)
            #  Else, handle the wrong character
            else:
                if self.handle_wrong(char):
                    continue
                else:
                    break
        self.handle_incomplete()
        return self

    def run(self, input_file: List[str]) -> Tuple[int, int]:
        # Reset the object
        self._reset()
        # Iterate over the lines
        for line in input_file:
            self.iterate_line(line)
        # Return the two scores
        return (
            sum(self.wrong_scores),
            sorted(self.incomplete_scores)[int(len(self.incomplete_scores) / 2)],
        )


def main():
    input_file = read_input("2021/10/input.txt")

    line_iterator = LineIterator()
    res_1, res_2 = line_iterator.run(input_file)

    print(f"Result of part 1: {res_1}")
    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main()
