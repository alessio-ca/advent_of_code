from functools import reduce
from itertools import permutations
from typing import List, Tuple, Union

from utils import read_input, timefunc


class SnailMath:
    def __init__(self, numbers: List[str]):
        self.numbers = numbers

    def _candidate_numerics(self, s: str, inverse=False) -> Tuple[int, int]:
        sgn = -1 if inverse else 1
        # Check if there is a n-digit numeric at index i
        # Return n-digit digit numeric and offset
        offset = 0
        res = -1
        while s[offset].isnumeric():
            offset += 1
        if offset > 0:
            res = int(s[:offset][::sgn])
        return res, offset

    def _calc_magnitude(self, x: Union[List, int]) -> int:
        # Perform magnitude calculation recursively
        if isinstance(x, list):
            if any(isinstance(i, list) for i in x):
                return 3 * self._calc_magnitude(x[0]) + 2 * self._calc_magnitude(x[1])
            else:
                return 3 * x[0] + 2 * x[1]
        else:
            return x

    def _find_candidate(self, s: str, inverse=False) -> Tuple[int, int, int]:
        # Loop over string to find a numeric candidate
        j = 0
        kz = 0
        while j < len(s):
            z, kz = self._candidate_numerics(s[j:], inverse)
            if z != -1:
                return z, j, kz
            j += 1
        # Return the candidate, index and candidate size
        return -1, j, kz

    def _adjust_string(self, s: str, pair_n: int, inverse=False) -> tuple[str, int]:
        # Adjust string after finding a regular for the explosion
        sgn = -1 if inverse else 1
        # Loop string until a numeric if found.
        regular, j, k = self._find_candidate(s, inverse)
        # Adjust string if regular was found
        if regular != -1:
            regular_s = str(regular + pair_n)
            return s[:j] + regular_s[::sgn] + s[j + k :], j + k
        else:
            return s, 0

    def explode(self, s: str, i: int) -> Tuple[bool, str, int]:
        # Individuate numerics and offsets
        x, kx = self._candidate_numerics(s[i + 1 :])
        y, ky = self._candidate_numerics(s[i + 2 + kx :])
        # Check we have a pair
        is_alpha = (x != -1) and (y != -1)
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
            s_back, min_offset = self._adjust_string(s_back, x, inverse=True)
            # Find right side candidate and adjust forward string
            s_forward, _ = self._adjust_string(s_forward, y, inverse=False)

            # Create final string after explosion
            s = s_back[::-1] + s[offset_back] + "0" + s[offset_forward - 1] + s_forward
        else:
            pass

        return is_alpha, s, i - min_offset - 1

    def split(self, s: str, i: int) -> str:
        # Obtain left and right numbers
        number_to_split = int(s[i : i + 2])
        left_n = number_to_split // 2
        right_n = left_n + number_to_split % 2

        # Adjust string
        s = s[:i] + "[" + str(left_n) + "," + str(right_n) + "]" + s[i + 2 :]
        return s

    def post_explode(self, res: str, rollback_i: int, split_i: int) -> Tuple[int, bool]:
        # Do post-operations after explosions
        for roll_j, roll_char in enumerate(res[:rollback_i][::-1]):
            if roll_char == "[":
                rollback_i -= roll_j + 1
                break

        return rollback_i, False if rollback_i <= split_i else True

    def reduce(self, res: str) -> str:
        # Perform reduction until the number is reduced
        i = 0
        rollback_i = 0
        opened_dict = {}
        opened_dict[0] = 0
        split_i = len(res)
        to_split = False
        while i < (len(res) - 3):
            opened = opened_dict[rollback_i]
            # Parse the number and check for explosions (skip last bracket)
            for i, char in enumerate(res[rollback_i:-1], rollback_i):
                opened_dict[i] = opened
                # Open a new pair
                if char == "[":
                    opened += 1
                    # If we are opening a nested pair at more than 4, performe explode
                    if opened > 4:
                        stop, res, rollback_i = self.explode(res, i)
                        #  If there has been an explosion, stop and
                        #  reset split if rollback is smaller
                        #  than the existing candidate split
                        if stop:
                            rollback_i, to_split = self.post_explode(
                                res, rollback_i, split_i
                            )
                            break
                # Close a pair
                elif char == "]":
                    opened -= 1
                # Check if there is a pair of consecutive numerics (which means the
                #  number is arger than 9). Mark split candidate
                elif (not to_split) and ((char + res[i + 1]).isnumeric()):
                    split_i = min(i, split_i)
                    to_split = True

            # If there are no explosions, perform the split if there is a candidate
            if (to_split) and (i >= (len(res) - 3)):
                i = split_i
                rollback_i = i
                res = self.split(res, i)
                split_i = len(res)
                to_split = False
        return res

    def add(self, s1: str, s2: str) -> str:
        # Perform addition between two numbers
        return "[" + s1 + "," + s2 + "]"

    def do_math(self, x: str, y: str) -> str:
        return self.reduce(self.add(x, y))

    def process(self) -> int:
        res = reduce(self.do_math, self.numbers)
        return self._calc_magnitude(eval(res))


@timefunc
def main():
    input_file = read_input("2021/18/input.txt")
    snail_numbers = SnailMath(input_file)
    res = snail_numbers.process()
    print(f"Result of part 1: {res}")

    # Generate all possible distinct pairs
    pairs = permutations(input_file, 2)
    max_m = 0
    for _, pair in enumerate(pairs):
        pair_numbers = SnailMath(pair)
        max_m = max(max_m, pair_numbers.process())
    print(f"Result of part 2: {max_m}")


if __name__ == "__main__":
    main()
