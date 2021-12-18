from utils import read_input
from typing import List, Union, Tuple
import itertools


class SnailMath:
    def __init__(self, numbers: List[str]):
        self.numbers = numbers

    def _candidate_numerics(self, s: str) -> Tuple[str, int]:
        # Check if there is a n-digit numeric at index i
        # Return n-digit digit numeric and offset
        offset = 1
        while s[:offset].isnumeric():
            offset += 1
        return s[: offset - 1], offset - 1

    def _calc_magnitude(self, x: Union[List, int]) -> int:
        # Perform magnitude calculation recursively
        if isinstance(x, list):
            if any(isinstance(i, list) for i in x):
                return 3 * self._calc_magnitude(x[0]) + 2 * self._calc_magnitude(x[1])
            else:
                return 3 * x[0] + 2 * x[1]
        else:
            return x

    def add(self, s1: str, s2: str) -> str:
        # Perform addition between two numbers
        return "[" + s1 + "," + s2 + "]"

    def explode(self, s: str, i: int) -> Tuple[bool, str, int]:
        # Individuate numerics
        x, kx = self._candidate_numerics(s[i + 1 :])
        y, ky = self._candidate_numerics(s[i + 2 + kx :])
        # Check we have a pair
        is_alpha = (x + y).isnumeric()
        if is_alpha:
            # Loop back string until a numeric if found.
            #  Add the first number of the pair to it
            j = i - 2  # There is always a comma before an eventual number
            left_regular = None
            while j > 0:
                z, kz = self._candidate_numerics(s[j::-1])
                if z.isnumeric():
                    left_regular = str(int(z[::-1]) + int(x))
                    break
                j -= 1
            # If a left regular was found, adjust string and iterator variable
            if left_regular:
                s = s[: j - kz + 1] + left_regular + s[j + 1 :]
                # Adjust by the difference between the new inserted number
                #  and the previous one
                i += len(left_regular) - kz

            # Loop forward string until a numeric if found.
            #  Add the second number of the pair to it
            j = (
                i + kx + ky + 4
            )  # There is always a comma and a closing bracket before an eventual number
            right_regular = None
            while j < len(s):
                z, kz = self._candidate_numerics(s[j:])
                if z.isnumeric():
                    right_regular = str(int(z) + int(y))
                    break
                j += 1
            # If a right regular was found, adjust string
            if right_regular:
                s = s[:j] + right_regular + s[j + kz :]

            # Replace pair with 0
            s = s[:i] + "0" + s[(i + kx + ky + 3) :]
        else:
            pass

        return is_alpha, s, i

    def split(self, s: str, i: int) -> str:
        # Obtain left and right numbers
        number_to_split = int(s[i : i + 2])
        left_n = number_to_split // 2
        right_n = left_n + number_to_split % 2

        # Adjust string
        s = s[:i] + "[" + str(left_n) + "," + str(right_n) + "]" + s[i + 2 :]

        return s

    def reduce(self, res: str) -> str:
        # Perform reduction until the number is reduced
        i = 0
        while i != len(res) - 1:
            opened = 0
            to_split_i = -1
            # Parse the number and check for explosions
            for i, char in enumerate(res):
                # Open a new pair
                if char == "[":
                    opened += 1
                    # If we are opening a nested pair at more than 4, performe explode
                    if opened > 4:
                        stop, res, i = self.explode(res, i)
                        #  If there has been an explosion, stop and
                        #  reset split candidate
                        if stop:
                            to_split_i = -1
                            break
                # Close a pair
                elif char == "]":
                    opened -= 1
                # Check if there is a pair of consecutive numerics (which means the
                #  number is arger than 9). Mark split candidate
                elif ((char + res[i + 1]).isnumeric()) and (to_split_i < 0):
                    to_split_i = i
            # If there are no explosions, perform the split if there is a candidate
            if to_split_i > 0:
                i = to_split_i
                res = self.split(res, i)

        return res

    def process(self) -> int:
        res = self.numbers[0]
        for el in self.numbers[1:]:
            res = self.add(res, el)
            res = self.reduce(res)
        return self._calc_magnitude(eval(res))


def main():
    input_file = read_input("2021/18/input.txt")
    snail_numbers = SnailMath(input_file)
    res = snail_numbers.process()
    print(f"Result of part 1: {res}")

    # Generate all possible distinct pairs
    pairs = itertools.permutations(input_file, 2)
    max_m = 0
    for pair in pairs:
        pair_numbers = SnailMath(pair)
        max_m = max(max_m, pair_numbers.process())
    print(f"Result of part 2: {max_m}")


if __name__ == "__main__":
    main()
