from utils import read_input
from typing import List, Union, Tuple
from itertools import permutations
from functools import reduce


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

    def _find_candidate(self, s: str) -> Tuple[str, int, int]:
        # Loop over string to find a numeric candidate
        regular = ""
        j = 0
        kz = 0
        while j < len(s):
            z, kz = self._candidate_numerics(s[j:])
            if z.isnumeric():
                return z, j, kz
            j += 1
        # Return the candidate, index and candidate size
        return regular, j, kz

    def _adjust_string(self, s: str, pair_n: str, inverse=False) -> str:
        # Adjust string after finding a regular for the explosion
        sgn = -1 if inverse else 1
        # Loop string until a numeric if found.
        regular, j, k = self._find_candidate(s)
        # Adjust string if regular was found
        regular = str(int(regular[::sgn]) + int(pair_n)) if regular else regular
        return s[:j] + regular[::sgn] + s[j + k :]

    def explode(self, s: str, i: int) -> Tuple[bool, str, int]:
        # Individuate numerics and offsets
        x, kx = self._candidate_numerics(s[i + 1 :])
        y, ky = self._candidate_numerics(s[i + 2 + kx :])
        # Check we have a pair
        is_alpha = (x + y).isnumeric()
        if is_alpha:
            # Split string in two.
            # For the back, only consider down to 1 spaces from the current
            #  (since there is always a comma before a candidate number)
            # For the forward, only consider up to 4 + (kx, ky) spaces from the current
            #  (since there are the number digits, two commas and brackets before a
            #  candidate number)
            offset_back = i - 1
            offset_forward = i + kx + ky + 4
            s_back, s_forward = s[:offset_back][::-1], s[offset_forward:]

            # Find left side candidate and adjust back string
            s_back = self._adjust_string(s_back, x, inverse=True)
            # Find right side candidate and adjust forward string
            s_forward = self._adjust_string(s_forward, y, inverse=False)

            # Create final string after explosion
            s = s_back[::-1] + s[offset_back] + "0" + s[offset_forward - 1] + s_forward
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
        while i < (len(res) - 3):
            opened = 0
            to_split_i = -1
            # Parse the number and check for explosions (skip last bracket)
            for i, char in enumerate(res[:-1]):
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
                elif (to_split_i < 0) and ((char + res[i + 1]).isnumeric()):
                    to_split_i = i
            # If there are no explosions, perform the split if there is a candidate
            if to_split_i > 0:
                i = to_split_i
                res = self.split(res, i)

        return res

    def add(self, s1: str, s2: str) -> str:
        # Perform addition between two numbers
        return "[" + s1 + "," + s2 + "]"

    def do_math(self, x: str, y: str) -> str:
        return self.reduce(self.add(x, y))

    def process(self) -> int:
        res = reduce(self.do_math, self.numbers)
        return self._calc_magnitude(eval(res))


def main():
    input_file = read_input("2021/18/input.txt")
    snail_numbers = SnailMath(input_file)
    res = snail_numbers.process()
    print(f"Result of part 1: {res}")

    # Generate all possible distinct pairs
    pairs = permutations(input_file, 2)
    max_m = 0
    for pair in pairs:
        pair_numbers = SnailMath(pair)
        max_m = max(max_m, pair_numbers.process())
    print(f"Result of part 2: {max_m}")


if __name__ == "__main__":
    main()
