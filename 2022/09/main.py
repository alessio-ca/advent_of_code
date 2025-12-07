from typing import List

from utils import read_input


def move_tail(head: List[int], tail: List[int]) -> bool:
    # Check whether head and tail are adjacent
    return max(abs(val1 - val2) for val1, val2 in zip(head, tail)) > 1


def rope_walk(n_tails: int, moves: List[str]) -> int:
    # Define initial quantities
    head = [0, 0]
    tails = [[0, 0] for _ in range(n_tails)]
    set_tail_positions = set()
    set_tail_positions.add(tuple(tails[-1]))

    # Iterate over moves
    for move in moves:
        direction, steps_str = move.split(" ")
        steps = int(steps_str)
        idx_par = 0 if direction in ["R", "L"] else 1

        while steps > 0:
            # Move head
            move_h = -1 + 2 * (direction in ["R", "U"])
            head[idx_par] += move_h

            # Loop over tails -- start with current head and tail 0
            current_head = head.copy()
            i = 0
            while move_tail(current_head, tails[i]):
                # If check is True, tail needs to move
                # Perform diagonal or horizontal move for each axis
                for axis in [0, 1]:
                    move_h = -1 + 2 * (current_head[axis] - tails[i][axis] > 0)
                    tails[i][axis] += move_h * (
                        (current_head[axis] - tails[i][axis]) != 0
                    )

                # Update current head to be the current tail & advance tail index
                current_head = tails[i].copy()
                i += 1
                # If we just moved the last tail, update set of visited positions
                if i == len(tails):
                    set_tail_positions.add(tuple(tails[-1]))
                    break

            steps -= 1

    return len(set_tail_positions)


def main(filename: str):
    moves = read_input(filename, line_strip=True)
    print(f"Result of part 1: {rope_walk(1, moves)}")
    print(f"Result of part 2: {rope_walk(9, moves)}")


if __name__ == "__main__":
    main("2022/09/input.txt")
