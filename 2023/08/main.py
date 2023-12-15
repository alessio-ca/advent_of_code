from utils import read_input_batch
import regex as re
from itertools import cycle
import numpy as np


def cond_part_1(key):
    return key != "ZZZ"


def cond_part_2(key):
    return key[-1] != "Z"


class Network:
    def __init__(self, network, instr) -> None:
        self.network = network
        self.instr = instr

    def navigate_network(self, key, cond):
        directions = cycle(self.instr)
        n = 0
        while cond(key):
            step = next(directions)
            key = self.network[key][step]
            n += 1
        return n

    def human_navigate_network(self):
        return self.navigate_network("AAA", lambda x: cond_part_1(x))

    def ghost_navigate_network(self):
        keys = [key for key in self.network if key[-1] == "A"]
        paths = (self.navigate_network(key, lambda x: cond_part_2(x)) for key in keys)
        return np.lcm.reduce(list(paths))


def main():
    instr, network = read_input_batch("2023/08/input.txt", line_split=False)
    network = {
        x: (y, z) for (x, y, z) in (re.findall(r"[A-Z]{3}", line) for line in network)
    }
    instr = [0 if x == "L" else 1 for x in instr[0]]

    problem_network = Network(network, instr)
    print(f"Result of part 1: {problem_network.human_navigate_network()}")
    print(f"Result of part 2: {problem_network.ghost_navigate_network()}")


if __name__ == "__main__":
    main()
