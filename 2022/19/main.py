import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any
from utils import read_input, timefunc


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def create_blueprints(raw_input):
    blueprints = {}
    for i, line in enumerate(raw_input):
        blueprints[i] = []
        for instr in line.split("."):
            if instr:
                match = [
                    group
                    for group in re.fullmatch(
                        r"^Each ([a-z]+) robot costs (\d+) ([a-z]+)"
                        r"(?: and (\d+) ([a-z]+))*$",
                        instr.strip(),
                    ).groups()
                    if group is not None
                ]
                key = match.pop(0)
                costs = defaultdict(
                    int, {ore: int(cost) for (cost, ore) in chunks(match, 2)}
                )
                blueprints[i].append(Robot(key, costs))

    return blueprints


def potential_ore(resource, robots, time):
    return resource + time * robots


@dataclass
class Robot:
    type: int
    ore: int
    clay: int
    obsidian: int

    def __init__(self, type, costs):
        # Initialise type
        if type == "ore":
            self.type = 0
        elif type == "clay":
            self.type = 1
        elif type == "obsidian":
            self.type = 2
        else:
            self.type = 3

        # Initialise costs
        self.oe_cost = costs["ore"]
        self.c_cost = costs["clay"]
        self.ob_cost = costs["obsidian"]


TRI_NUMBERS = [(i - 1) * i // 2 for i in range(33)]


# Operations have been optimised by avoiding lists
class MiningOp:
    def __init__(self, blueprint, time) -> None:
        self.time = time
        # Order is: ore, clay, obsidian, geode
        self.active_robots = (1, 0, 0, 0)
        self.resources = (0, 0, 0, 0)
        self.max_requirements = tuple(
            list(
                max(getattr(robot, key) for robot in blueprint)
                for key in ["oe_cost", "c_cost", "ob_cost"]
            )
            + [self.time]
        )
        self.blueprint = blueprint
        self.max_geodes = 0
        self.best_geodes: defaultdict[Any, int] = defaultdict(int)
        pass

    def op_potential(self, time, *args):
        _, _, _, g, _, _, _, g_r = args
        return g + g_r * time + TRI_NUMBERS[time]

    def too_many_robots(self, robot, *args):
        oe_max, c_max, ob_max, _ = self.max_requirements
        _, _, _, _, oe_r, c_r, ob_r, _ = args
        if (
            robot.type == 0
            and oe_r >= oe_max
            or robot.type == 1
            and c_r >= c_max
            or robot.type == 2
            and (ob_r >= ob_max or c_r == 0)
            or robot.type == 3
            and ob_r == 0
        ):
            return True
        return False

    def augment_ore(self, *args):
        oe_cost, oe, c, ob, g, oe_r, c_r, ob_r, g_r = args
        return (
            oe - oe_cost + oe_r,
            c + c_r,
            ob + ob_r,
            g + g_r,
            oe_r + 1,
            c_r,
            ob_r,
            g_r,
        )

    def augment_clay(self, *args):
        oe_cost, oe, c, ob, g, oe_r, c_r, ob_r, g_r = args
        return (
            oe - oe_cost + oe_r,
            c + c_r,
            ob + ob_r,
            g + g_r,
            oe_r,
            c_r + 1,
            ob_r,
            g_r,
        )

    def augment_obsidian(self, *args):
        oe_cost, c_cost, oe, c, ob, g, oe_r, c_r, ob_r, g_r = args
        return (
            oe - oe_cost + oe_r,
            c - c_cost + c_r,
            ob + ob_r,
            g + g_r,
            oe_r,
            c_r,
            ob_r + 1,
            g_r,
        )

    def augment_geode(self, *args):
        oe_cost, ob_cost, oe, c, ob, g, oe_r, c_r, ob_r, g_r = args
        return (
            oe - oe_cost + oe_r,
            c + c_r,
            ob - ob_cost + ob_r,
            g + g_r,
            oe_r,
            c_r,
            ob_r,
            g_r + 1,
        )

    def target_op(self, time, robot, *args):
        oe, c, ob, g, oe_r, c_r, ob_r, g_r = args
        # Pruning operations
        # 1. Check if branch is underperforming
        if self.best_geodes[time] > g:
            return None
        else:
            self.best_geodes[time] = g
        # 2. Check if branch has low potential
        if self.op_potential(time, *args) <= self.max_geodes:
            return None
        # 3. Check if we have too many robots
        if self.too_many_robots(robot, *args):
            return None

        # If branch survives, enter time loop
        while time > 0:
            # Check if you can build the target robot
            # If you can, perform the necessary agumentation
            # Then, recurse all possible robots as new targets

            if robot.type == 0 and oe >= (oe_cost := getattr(robot, "oe_cost")):
                new_args = self.augment_ore(oe_cost, *args)
                for new_robot in self.blueprint:
                    self.target_op(time - 1, new_robot, *new_args)
                return None

            elif robot.type == 1 and oe >= (oe_cost := getattr(robot, "oe_cost")):
                new_args = self.augment_clay(oe_cost, *args)
                for new_robot in self.blueprint:
                    self.target_op(time - 1, new_robot, *new_args)
                return None

            elif (
                robot.type == 2
                and oe >= (oe_cost := getattr(robot, "oe_cost"))
                and c >= (c_cost := getattr(robot, "c_cost"))
            ):
                new_args = self.augment_obsidian(oe_cost, c_cost, *args)
                for new_robot in self.blueprint:
                    self.target_op(time - 1, new_robot, *new_args)
                return None

            elif (
                robot.type == 3
                and oe >= (oe_cost := getattr(robot, "oe_cost"))
                and ob >= (ob_cost := getattr(robot, "ob_cost"))
            ):
                new_args = self.augment_geode(oe_cost, ob_cost, *args)
                for new_robot in self.blueprint:
                    self.target_op(time - 1, new_robot, *new_args)
                return None

            time, oe, c, ob, g = time - 1, oe + oe_r, c + c_r, ob + ob_r, g + g_r
            args = oe, c, ob, g, oe_r, c_r, ob_r, g_r

        self.max_geodes = max(self.max_geodes, g)
        return None

    def optimise_op(self):
        for robot in self.blueprint:
            self.target_op(self.time, robot, *self.resources, *self.active_robots)
        return None


@timefunc
def main(filename: str):
    blueprints = create_blueprints(
        [line.split(": ")[1] for line in read_input(filename, line_strip=True)]
    )
    res = 0
    for id, blueprint in blueprints.items():
        op = MiningOp(blueprint, 24)
        op.optimise_op()
        res += op.max_geodes * (id + 1)

    print(f"Result of part 1: {res}")

    res = 1
    subset_blueprints = {k: blueprints[k] for k in range(3)}
    for id, blueprint in subset_blueprints.items():
        op = MiningOp(blueprint, 32)
        op.optimise_op()
        res *= op.max_geodes

    print(f"Result of part 2: {res}")


if __name__ == "__main__":
    main("2022/19/input.txt")
