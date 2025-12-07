import re
from math import floor, lcm, prod
from typing import List

from utils import read_input_batch


class Monkey:
    def __init__(self, params: List[str]) -> None:
        # Query monkey parameters
        search_int = re.compile(r"\d+")

        match = search_int.search(params[0])
        self.num = int(match.group()) if match else 0
        self.items = list(map(int, re.findall(r"\d+", params[1])))
        self.operation = eval("lambda old: " + params[2].split("=")[1])

        match = search_int.search(params[3])
        self.divisor = int(match.group()) if match else 1
        self.test = lambda x: x % self.divisor == 0
        match = search_int.search(params[4])
        self.throw_true = int(match.group()) if match else 0
        match = search_int.search(params[5])
        self.throw_false = int(match.group()) if match else 0

        self.inspected = 0


class MonkeyBusiness:
    def __init__(self, raw_monkeys) -> None:
        # Initialise monkeys and least common multiple
        self.monkeys = [Monkey(monkey) for monkey in raw_monkeys]
        self.maximum_divisor = lcm(*(monkey.divisor for monkey in self.monkeys))

    def inspect(self, monkey: Monkey, is_first_part=True):
        try:
            # Inspect the first element in line
            monkey.inspected += 1
            element = monkey.items.pop(0)

            # Apply worry level control
            if is_first_part:
                level = floor(monkey.operation(element) / 3)
            else:
                level = monkey.operation(element) % self.maximum_divisor

            # Perform test and throw
            test = monkey.test(level)
            if test:
                idx = monkey.throw_true
            else:
                idx = monkey.throw_false
            self.monkeys[idx].items.append(level)

        except IndexError:
            pass

    def round(self, is_first_part=True):
        # Iterate over all monkeys
        for i in range(len(self.monkeys)):
            # Iterate over all items in a monkey' possession
            for _ in range(len(self.monkeys[i].items)):
                self.inspect(self.monkeys[i], is_first_part)

    def play(self, is_first_part=True):
        # Simulate the game
        if is_first_part:
            num_round = 20
        else:
            num_round = 10000

        for _ in range(num_round):
            self.round(is_first_part)


def main(filename: str):
    monkeys_raw = read_input_batch(filename, line_split=False)
    monkey_problem = MonkeyBusiness(monkeys_raw)
    monkey_problem.play()
    times_inspected = [monkey.inspected for monkey in monkey_problem.monkeys]
    print(f"Result of part 1: {prod(sorted(times_inspected)[-2:])}")

    monkey_problem = MonkeyBusiness(monkeys_raw)
    monkey_problem.play(is_first_part=False)
    times_inspected = [monkey.inspected for monkey in monkey_problem.monkeys]
    print(f"Result of part 2: {prod(sorted(times_inspected)[-2:])}")


if __name__ == "__main__":
    main("2022/11/input.txt")
