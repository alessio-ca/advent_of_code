from utils import read_input
import numpy as np
from collections import Counter

def beam_splitter(diagram: np.ndarray, splitters: list[tuple[int,int]], y_start: int) -> tuple[int,int]:
    beams = [y_start]
    count = 0
    counter = Counter(beams)

    splitters_set = set(splitters)
    for row in range(1, diagram.shape[0]):
        new_beams = set()
        for _ in range(len(beams)):
            if beams:
                beam = beams.pop()
                if (row, beam) in splitters_set:
                    new_beams.add(beam - 1)
                    counter[beam - 1] += counter[beam] 
                    new_beams.add(beam + 1)
                    counter[beam + 1] += counter[beam] 
                    counter[beam] = 0
                    count += 1
                else:
                    new_beams.add(beam)
            else:
                break
        beams = list(new_beams)

    return count, sum(counter.values())


def main(filename: str):
    diagram = np.array([list(line) for line in read_input(filename)], dtype=str)
    y_start = np.where(diagram == 'S')[1][0]
    x_splitter, y_splitter = np.where(diagram == '^')
    splitters = list(zip(x_splitter, y_splitter))
    count, counter = beam_splitter(diagram, splitters, y_start)
    print(f"Result of part 1: {count}")
    print(f"Result of part 2: {counter}")


if __name__ == "__main__":
    main("2025/07/input.txt")
